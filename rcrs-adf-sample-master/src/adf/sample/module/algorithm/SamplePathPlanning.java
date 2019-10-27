package adf.sample.module.algorithm;

import adf.agent.communication.MessageManager;
import adf.agent.develop.DevelopData;
import adf.agent.info.AgentInfo;
import adf.agent.info.ScenarioInfo;
import adf.agent.info.WorldInfo;
import adf.agent.module.ModuleManager;
import adf.agent.precompute.PrecomputeData;
import adf.component.module.algorithm.PathPlanning;
import rescuecore2.misc.collections.LazyMap;
import rescuecore2.standard.entities.Area;
import rescuecore2.worldmodel.Entity;
import rescuecore2.worldmodel.EntityID;

import java.util.*;

public class SamplePathPlanning extends PathPlanning {

    private Map<EntityID, Set<EntityID>> graph;
    private EntityID from;
    private Collection<EntityID> targets;
    private List<EntityID> result;

    public SamplePathPlanning(AgentInfo ai, WorldInfo wi, ScenarioInfo si, ModuleManager moduleManager, DevelopData developData) {
        super(ai, wi, si, moduleManager, developData);
        this.init();
    }

    private void init() {
        Map<EntityID, Set<EntityID>> neighbours = new LazyMap<EntityID, Set<EntityID>>() {
            @Override
            public Set<EntityID> createValue() {
                return new HashSet<>();
            }
        };
        for (Entity next : this.worldInfo) {
            if (next instanceof Area) {
                Collection<EntityID> areaNeighbours = ((Area) next).getNeighbours();
                neighbours.get(next.getID()).addAll(areaNeighbours);
            }
        }
        this.graph = neighbours;
    }

    @Override
    public List<EntityID> getResult() {
        return this.result;
    }

    @Override
    public PathPlanning setFrom(EntityID id) {
        this.from = id;
        return this;
    }

  //********Written by Animesh**********//
	public static int isParseInt(String str){
	        
	        int num = -1;
	        try{
	             num = Integer.parseInt(str);
	        } catch (NumberFormatException e) {
	        }
	        
	        return num;
	    }
	
//	public static <T, U> List<U> 
//    convertStringListToIntList(List<T> listOfString, 
//                               Function<T, U> function) 
//    { 
//        return listOfString.stream() 
//            .map(function) 
//            .collect(Collectors.toList()); 
//    } 
//	--------------------------------------------------------------------DO NOT EDIT------------------------------------------	
    @Override
    public PathPlanning setDestination(Collection<EntityID> targets) {
//        this.targets = targets;
//        System.out.println("AgentInfo" + this.agentInfo.getX());
//    	System.out.println("Building Ids" + this.worldInfo.getAllEntities());	 
			 this.targets = targets;		
			 return this;
		 }

//    	--------------------------------------------------------------------DO NOT EDIT------------------------------------------	
	
//    		   System.out.println("+++++++++++++++++++++++++++++++++++" + this.worldInfo.getFireBuildingIDs());
//    		   FireBrigade agent = (FireBrigade) agentInfo.me();
//    		   EntityID agentID = agentInfo.getID();
//    		   System.out.println(agentID.getValue() == 1127015061);
//    		   if (agentID.getValue() == 1127015061) {
//    			   targets11 = this.worldInfo.getFireBuildingIDs(); 
//    		   } else {
//    			   targets22 = this.worldInfo.getFireBuildingIDs();
//    		   }
////    		   System.out.println("THIS IS TARGET 11--------------------------------" + targets11);
////    		   System.out.println("IS TARGET11 null or empty------------------------" + (targets11 == null || targets11.isEmpty()));
////    		   System.out.println("THIS IS TARGET 22--------------------------------" + targets22);
////    		   System.out.println("IS TARGET22 null or empty------------------------" + (targets22 == null || targets22.isEmpty()));
//    		   
//    		   this.targets = targets;
//    		   
//    		   return this;
//    			--------------------------------------------------------------------DO NOT EDIT------------------------------------------				   

////    		//********Written by Animesh**********//
//        	ArrayList<EntityID> target_points = new ArrayList<EntityID>();
//        	EntityID a1 = new EntityID(298);
//        	target_points.add(a1);
//            this.targets = target_points;
//            return this;
//        	--------------------------------------------------------------------DO NOT EDIT------------------------------------------

    @Override
    public PathPlanning updateInfo(MessageManager messageManager) {
        super.updateInfo(messageManager);
        return this;
    }

    @Override
    public PathPlanning precompute(PrecomputeData precomputeData) {
        super.precompute(precomputeData);
        return this;
    }

    @Override
    public PathPlanning resume(PrecomputeData precomputeData) {
        super.resume(precomputeData);
        return this;
    }

    @Override
    public PathPlanning preparate() {
        super.preparate();
        return this;
    }

    @Override
    public PathPlanning calc() {
        List<EntityID> open = new LinkedList<>();
        Map<EntityID, EntityID> ancestors = new HashMap<>();
        open.add(this.from);
        EntityID next;
        boolean found = false;
        ancestors.put(this.from, this.from);
        do {
            next = open.remove(0);
            if (isGoal(next, targets)) {
                found = true;
                break;
            }
            Collection<EntityID> neighbours = graph.get(next);
            if (neighbours.isEmpty()) {
                continue;
            }
            for (EntityID neighbour : neighbours) {
                if (isGoal(neighbour, targets)) {
                    ancestors.put(neighbour, next);
                    next = neighbour;
                    found = true;
                    break;
                }
                else {
                    if (!ancestors.containsKey(neighbour)) {
                        open.add(neighbour);
                        ancestors.put(neighbour, next);
                    }
                }
            }
        } while (!found && !open.isEmpty());
        if (!found) {
            // No path
            this.result = null;
        }
        // Walk back from goal to this.from
        EntityID current = next;
        LinkedList<EntityID> path = new LinkedList<>();
        do {
            path.add(0, current);
            current = ancestors.get(current);
            if (current == null) {
                throw new RuntimeException("Found a node with no ancestor! Something is broken.");
            }
        } while (current != this.from);
        this.result = path;
        return this;
    }

    private boolean isGoal(EntityID e, Collection<EntityID> test) {
        return test.contains(e);
    }
}
