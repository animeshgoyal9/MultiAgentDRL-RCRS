package adf.sample.tactics;

import adf.agent.action.Action;
import adf.agent.action.common.ActionMove;
import adf.agent.action.common.ActionRest;
import adf.agent.communication.MessageManager;
import adf.agent.communication.standard.bundle.centralized.CommandScout;
import adf.agent.develop.DevelopData;
import adf.agent.info.AgentInfo;
import adf.agent.info.ScenarioInfo;
import adf.agent.info.WorldInfo;
import adf.agent.module.ModuleManager;
import adf.agent.precompute.PrecomputeData;
import adf.debug.WorldViewLauncher;
import adf.component.centralized.CommandExecutor;
import adf.component.communication.CommunicationMessage;
import adf.component.extaction.ExtAction;
import adf.component.module.complex.Search;
import adf.sample.tactics.utils.MessageTool;
import rescuecore2.standard.entities.*;
import rescuecore2.worldmodel.EntityID; 
import rescuecore2.score.*;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import adf.agent.action.fire.ActionExtinguish;
import adf.agent.action.fire.ActionRefill;
import adf.agent.communication.standard.bundle.centralized.CommandFire;
import adf.agent.communication.standard.bundle.information.MessageFireBrigade;
import adf.component.module.complex.BuildingDetector;
import adf.component.tactics.TacticsFireBrigade;
import firesimulator.FireSimulatorWrapper;

public class SampleTacticsFireBrigade extends TacticsFireBrigade
{
    private BuildingDetector buildingDetector;
    private Search search;

    private ExtAction actionFireFighting;
    private ExtAction actionExtMove;

    private CommandExecutor<CommandFire> commandExecutorFire;
    private CommandExecutor<CommandScout> commandExecutorScout;

    private MessageTool messageTool;

    private CommunicationMessage recentCommand;

	private Boolean isVisualDebug;
	private ScoreFunction score;
	private FireSimulatorWrapper firewrapper; 

    @Override
    public void initialize(AgentInfo agentInfo, WorldInfo worldInfo, ScenarioInfo scenarioInfo, ModuleManager moduleManager, MessageManager messageManager, DevelopData developData)
    {
        messageManager.setChannelSubscriber(moduleManager.getChannelSubscriber("MessageManager.PlatoonChannelSubscriber", "adf.sample.module.comm.SampleChannelSubscriber"));
        messageManager.setMessageCoordinator(moduleManager.getMessageCoordinator("MessageManager.PlatoonMessageCoordinator", "adf.sample.module.comm.SampleMessageCoordinator"));

        worldInfo.indexClass(
                StandardEntityURN.ROAD,
                StandardEntityURN.HYDRANT,
                StandardEntityURN.BUILDING,
                StandardEntityURN.REFUGE,
                StandardEntityURN.GAS_STATION,
                StandardEntityURN.AMBULANCE_CENTRE,
                StandardEntityURN.FIRE_STATION,
                StandardEntityURN.POLICE_OFFICE
        );

        this.messageTool = new MessageTool(scenarioInfo, developData);

        this.isVisualDebug = (scenarioInfo.isDebugMode()
                            && moduleManager.getModuleConfig().getBooleanValue("VisualDebug", false));

        this.recentCommand = null;
        
        // init Algorithm Module & ExtAction
        switch  (scenarioInfo.getMode())
        {
            case PRECOMPUTATION_PHASE:
            case PRECOMPUTED:
                this.search = moduleManager.getModule("TacticsFireBrigade.Search", "adf.sample.module.complex.SampleSearch");
                this.buildingDetector = moduleManager.getModule("TacticsFireBrigade.BuildingDetector", "adf.sample.module.complex.SampleBuildingDetector");
                this.actionFireFighting = moduleManager.getExtAction("TacticsFireBrigade.ActionFireFighting", "adf.sample.extaction.ActionFireFighting");
                this.actionExtMove = moduleManager.getExtAction("TacticsFireBrigade.ActionExtMove", "adf.sample.extaction.ActionExtMove");
                this.commandExecutorFire = moduleManager.getCommandExecutor("TacticsFireBrigade.CommandExecutorFire", "adf.sample.centralized.CommandExecutorFire");
                this.commandExecutorScout = moduleManager.getCommandExecutor("TacticsFireBrigade.CommandExecutorScout", "adf.sample.centralized.CommandExecutorScout");
                break;
            case NON_PRECOMPUTE:
                this.search = moduleManager.getModule("TacticsFireBrigade.Search", "adf.sample.module.complex.SampleSearch");
                this.buildingDetector = moduleManager.getModule("TacticsFireBrigade.BuildingDetector", "adf.sample.module.complex.SampleBuildingDetector");
                this.actionFireFighting = moduleManager.getExtAction("TacticsFireBrigade.ActionFireFighting", "adf.sample.extaction.ActionFireFighting");
                this.actionExtMove = moduleManager.getExtAction("TacticsFireBrigade.ActionExtMove", "adf.sample.extaction.ActionExtMove");
                this.commandExecutorFire = moduleManager.getCommandExecutor("TacticsFireBrigade.CommandExecutorFire", "adf.sample.centralized.CommandExecutorFire");
                this.commandExecutorScout = moduleManager.getCommandExecutor("TacticsFireBrigade.CommandExecutorScout", "adf.sample.centralized.CommandExecutorScout");
                break;
        }

        registerModule(this.buildingDetector);
        registerModule(this.search);
        registerModule(this.actionFireFighting);
        registerModule(this.actionExtMove);
        registerModule(this.commandExecutorFire);
        registerModule(this.commandExecutorScout);
    }

    @Override
    public void precompute(AgentInfo agentInfo, WorldInfo worldInfo, ScenarioInfo scenarioInfo, ModuleManager moduleManager, PrecomputeData precomputeData, DevelopData developData)
    {
        modulesPrecompute(precomputeData);
    }

    @Override
    public void resume(AgentInfo agentInfo, WorldInfo worldInfo, ScenarioInfo scenarioInfo, ModuleManager moduleManager, PrecomputeData precomputeData, DevelopData developData)
    {
        modulesResume(precomputeData);

        if (isVisualDebug)
        {
            WorldViewLauncher.getInstance().showTimeStep(agentInfo, worldInfo, scenarioInfo);
        }
    }
    

    @Override
    public void preparate(AgentInfo agentInfo, WorldInfo worldInfo, ScenarioInfo scenarioInfo, ModuleManager moduleManager, DevelopData developData)
    {
        modulesPreparate();

        if (isVisualDebug)
        {
            WorldViewLauncher.getInstance().showTimeStep(agentInfo, worldInfo, scenarioInfo);
        }
    }

    @Override
    public Action think(AgentInfo agentInfo, WorldInfo worldInfo, ScenarioInfo scenarioInfo, ModuleManager moduleManager, MessageManager messageManager, DevelopData developData)
    {
        this.messageTool.reflectMessage(agentInfo, worldInfo, scenarioInfo, messageManager);
        this.messageTool.sendRequestMessages(agentInfo, worldInfo, scenarioInfo, messageManager);
        this.messageTool.sendInformationMessages(agentInfo, worldInfo, scenarioInfo, messageManager);

        modulesUpdateInfo(messageManager);

        if (isVisualDebug)
        {
            WorldViewLauncher.getInstance().showTimeStep(agentInfo, worldInfo, scenarioInfo);
        }
        	
        FireBrigade agent = (FireBrigade) agentInfo.me();
        EntityID agentID = agentInfo.getID();
        // command
        for (CommunicationMessage message : messageManager.getReceivedMessageList(CommandScout.class))
        {
            CommandScout command = (CommandScout) message;
            if (command.isToIDDefined() && Objects.requireNonNull(command.getToID()).getValue() == agentID.getValue())
            {
                this.recentCommand = command;
                this.commandExecutorScout.setCommand(command);
            }
        }

        for (CommunicationMessage message : messageManager.getReceivedMessageList(CommandFire.class))
        {
            CommandFire command = (CommandFire) message;
            if (command.isToIDDefined() && Objects.requireNonNull(command.getToID()).getValue() == agentID.getValue())
            {
                this.recentCommand = command;
                this.commandExecutorFire.setCommand(command);
            }
        }

        if (this.recentCommand != null)
        {
            Action action = null;
            if (this.recentCommand.getClass() == CommandFire.class)
            {
                action = this.commandExecutorFire.calc().getAction();
            }
            else if (this.recentCommand.getClass() == CommandScout.class)
            {
                action = this.commandExecutorScout.calc().getAction();
            }

            if (action != null)
            {
            	EntityID a1 = new EntityID(248);
            	Building building1 = (Building) worldInfo.getEntity(a1); 
				this.sendActionMessage(messageManager, agent, action, agentInfo, worldInfo, score, building1);
                return action;
            }
        }
        // autonomous
        EntityID target = this.buildingDetector.calc().getTarget();
        Action action = this.actionFireFighting.setTarget(target).calc().getAction();
        if (action != null)
        {
        	EntityID a1 = new EntityID(248);
        	Building building1 = (Building) worldInfo.getEntity(a1);
            this.sendActionMessage(messageManager, agent, action, agentInfo, worldInfo, score, building1);
            return action;
        }
        target = this.search.calc().getTarget();
        action = this.actionExtMove.setTarget(target).calc().getAction();
        if (action != null)
        {
        	EntityID a1 = new EntityID(248);
        	Building building1 = (Building) worldInfo.getEntity(a1);
        	this.sendActionMessage(messageManager, agent, action, agentInfo, worldInfo, score, building1);
            return action;
        }

        messageManager.addMessage(
                new MessageFireBrigade(true, agent, MessageFireBrigade.ACTION_REST,  agent.getPosition())
        );
        return new ActionRest();
    }

    private void sendActionMessage(MessageManager messageManager, FireBrigade agent, Action action, AgentInfo agentInfo, WorldInfo worldInfo, ScoreFunction score, Building building)
    {
        Class<? extends Action> actionClass = action.getClass();
        int actionIndex = -1;
        EntityID target = null;
        if (actionClass == ActionMove.class)
        {
            actionIndex = MessageFireBrigade.ACTION_MOVE;
            List<EntityID> path = ((ActionMove) action).getPath();
            if (path.size() > 0)
            {
            	target = path.get(path.size() - 1);
                System.out.println("***********Start Moving**************");
                
                try {
                	//  		 Create a new list that is sent to python
                				 int X_value = (int) agentInfo.getX();
                				 int Y_value = (int) agentInfo.getY();
                				 ArrayList<Object> newList = new ArrayList<>();
                				 FireBrigade agent1 = (FireBrigade) agentInfo.me();
                				 EntityID agentID = agentInfo.getID();
                				 int buriedness = agent1.getBuriedness();
                				 int water = agent1.getWater();
                				 int damage = agent1.getDamage();
                	         	 int stamina = agent1.getStamina();
                	         	 int hp = agent1.getHP();
                				 int agent_id = (int) agentInfo.getID().getValue(); 
                				 
                				 if (agentID.getValue() == 210552869) {
                					 EntityID c1 = new EntityID(agent_id);   
                					 EntityID c2 = new EntityID(X_value);
                					 EntityID c3 = new EntityID(Y_value);
                					 EntityID c4 = new EntityID(hp);
                					 EntityID c5 = new EntityID(damage);
                					 EntityID c6 = new EntityID(stamina);
                					 EntityID c7 = new EntityID(buriedness);
                					 EntityID c8 = new EntityID(water);
                					 
                					 newList.add(c1);
                					 newList.add(c2);
                					 newList.add(c3);
                					 newList.add(c4);
                					 newList.add(c5);
                					 newList.add(c6);
                					 newList.add(c7);
                					 newList.add(c8);
                					 newList.add(worldInfo.getEntityIDsOfType(StandardEntityURN.BUILDING));
                				 } else {
                					 EntityID c9 = new EntityID(agent_id);   
                					 EntityID c10 = new EntityID(X_value);
                					 EntityID c11 = new EntityID(Y_value);
                					 EntityID c12 = new EntityID(hp);
                					 EntityID c13 = new EntityID(damage);
                					 EntityID c14 = new EntityID(stamina);
                					 EntityID c15 = new EntityID(buriedness);
                					 EntityID c16 = new EntityID(water);
                					 newList.add(c9);
                					 newList.add(c10);
                					 newList.add(c11);
                					 newList.add(c12);
                					 newList.add(c13);
                					 newList.add(c14);
                					 newList.add(c15);
                					 newList.add(c16);
                				 }
                				 
                	//  			 Open the socket
                				 Socket ss = new Socket("localhost", 2025);
                				 PrintWriter out = new PrintWriter(ss.getOutputStream(), true);
                	//  			 Send information to python
                				 out.println(newList);
                				 
                	//			--------------------------------------------------------------------DO NOT EDIT------------------------------------------			
                	           
                	//         System.out.println("AgentInfo" + agentInfo.getPositionArea());
                	//         System.out.println("Building Ids" + worldInfo.getAllEntities());
                	//         System.out.println("Building Temp" + building.getFullDescription());
                	//         System.out.println(agentID.getValue());
                	         
                	//         Building building1 = (Building) worldInfo.getEntity(buildingid);
                	         
                	         System.out.println("---------------------------Action Info---------------------------------");
                	         System.out.println("Building IDs: " + worldInfo.getEntityIDsOfType(StandardEntityURN.BUILDING));
                	        
                	         System.out.println("---------------------------State Info---------------------------------");
                	//         EntityID buildingid = new EntityID(959);
                	//         System.out.println("Building Full desc: " + worldInfo.getEntity(buildingid).getFullDescription());
                	         
                	//         System.out.println("Building fieryness: " + StandardPropertyURN.FIERYNESS.toString());
                	//         EntityID a1 = new EntityID(959);
                	//     	Building building1 = (Building) worldInfo.getEntity(a1);
                	//     	System.out.println("Building Fieryness: " + building1.getProperty(StandardPropertyURN.FIERYNESS.toString()));
                	//     	System.out.println("Building Area: " + building1.getProperty(StandardPropertyURN.BUILDING_AREA_TOTAL.toString()));
                	//     	System.out.println("Building Temperature: " + building1.getProperty(StandardPropertyURN.TEMPERATURE.toString()));
                	//     	System.out.println("Building X: " + building1.getX());
                	//     	System.out.println("Building Y: " + building1.getY());
                	//     	System.out.println("Building Fire: " + building1.isFierynessDefined());
                	     	
                	//     	if (building1.isFierynessDefined()){
                	//     		System.out.println("Building Fire-------------------: " + firewrapper);
                	//     	}
                	//     	if (building1.isTemperatureDefined()){
                	//     		System.out.println("Building Temp-------------------: " + building1.getTemperature());
                	//     	}
                	     	
                	//     	for (Entity next : model) {
                	//     		for (Object next1 : worldInfo.getEntityIDsOfType(StandardEntityURN.BUILDING)) {
                	//                 Building b = (Building)next1;
                	//                 Building oldB = (Building)model.getEntity(next1);
                	//                 if ((!oldB.isFierynessDefined()) || (oldB.getFieryness() != b.getFieryness())) {
                	//                     oldB.setFieryness(b.getFieryness());
                	//                     changes.addChange(oldB, oldB.getFierynessProperty());
                	//                 }
                	//                 if ((!oldB.isTemperatureDefined()) || (oldB.getTemperature() != (int)b.getTemperature())) {
                	//                     oldB.setTemperature((int)b.getTemperature());
                	//                     changes.addChange(oldB, oldB.getTemperatureProperty());
                	//                 }
                	//             }
                	//     	}
                	     	
                	//         System.out.println("Fire----------------------------------------------------------- " + firewrapper); 	
                	     	
                	         
                	         if (agentID.getValue() == 210552869) {
                	         	System.out.println("-----------------------------------------");
                	             System.out.println("THIS THE X: " + agentInfo.getX());
                	             System.out.println("THIS THE Y: " + agentInfo.getY());
                	             System.out.println("THIS THE ID: " + agentInfo.getID());
                	             System.out.println("THIS THE HP: " + hp);
                	             System.out.println("THIS THE Damage: " + damage);
                	             System.out.println("THIS THE Stamina: " + stamina);
                	             System.out.println("THIS THE Buriedness: " + buriedness);
                	             System.out.println("THIS THE Water level: " + water);
                	             System.out.println("------------------------------------------");
                	         } else {
                	         	System.out.println("-----------------------------------------");
                	             System.out.println("THIS THE X: " + agentInfo.getX());
                	             System.out.println("THIS THE Y: " + agentInfo.getY());
                	             System.out.println("THIS THE ID: " + agentInfo.getID());
                	             System.out.println("THIS THE HP: " + hp);
                	             System.out.println("THIS THE Damage: " + damage);
                	             System.out.println("THIS THE Stamina: " + stamina);
                	             System.out.println("THIS THE Buriedness: " + buriedness);
                	             System.out.println("THIS THE Water level: " + water);
                	             System.out.println("------------------------------------------");
                	         }
                	         
                	//			--------------------------------------------------------------------DO NOT EDIT------------------------------------------    
                				 
                	//  			 Take the data in from socket
                				 BufferedReader in = new BufferedReader(new InputStreamReader(ss.getInputStream()));
                	//  			 Create a string variable that stores the input
                				 String str;
                				 while((str = in.readLine()) != null) 
                				 {
                					 String replace = str.replace("[","");
                					 String replace1 = replace.replace("]","");
                	//  				 Split the list
                					 List<String> myList = new ArrayList<String>(Arrays.asList(replace1.split(", ")));
                	//  				 Convert string of list to list
                					 List<Integer> listOfInteger = myList.stream().map(s -> Integer.parseInt(s)).collect(Collectors.toList());
                	//  				 Print and check if everything is correct
                					 System.out.println("THIS IS THE PARSE INT STRING%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% "+ listOfInteger);
                					 
                	//  				 Add the integers to Array - targets1
                					 ArrayList<EntityID> targets1 = new ArrayList<EntityID>();
                					 EntityID a1= new EntityID(listOfInteger.get(0));
                					 targets1.add(a1);
//                					 this.targets = targets1;  
                	//  				 Flushing is important
                					 out.flush();
                				 }
                	//  			 Close the connection
                				 out.close();
                				 in.close();
                				 ss.close();
                			 	} catch (FileNotFoundException e) {
                	  			// TODO Auto-generated catch block
                	  			System.out.println(e);
                	  			e.printStackTrace();
                	  		} catch (IOException e) {
                	  			// TODO Auto-generated catch block
                	  			System.out.println(e);
                	  			e.printStackTrace();
                	  		} 
                
                
            }
        }
        else if (actionClass == ActionExtinguish.class)
        {
            actionIndex = MessageFireBrigade.ACTION_EXTINGUISH;
            target = ((ActionExtinguish)action).getTarget();
            System.out.println("***********Start Extinguishing**************");
        }
        else if (actionClass == ActionRefill.class)
        {
            actionIndex = MessageFireBrigade.ACTION_REFILL;
            target = agent.getPosition();
            System.out.println("***********Start Refilling**************");
        }
        else if (actionClass == ActionRest.class)
        {
            actionIndex = MessageFireBrigade.ACTION_REST;
            target = agent.getPosition();
            System.out.println("***********Start Resting**************");
        }

        if (actionIndex != -1)
        {
            messageManager.addMessage(new MessageFireBrigade(true, agent, actionIndex, target));
        }
    }

//	private Building Building(EntityID buildingid) {
//		// TODO Auto-generated method stub
//		return null;
//	}
}
