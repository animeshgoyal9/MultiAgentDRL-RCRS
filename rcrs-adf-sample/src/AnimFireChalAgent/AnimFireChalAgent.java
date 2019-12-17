package AnimFireChalAgent;

import java.util.Arrays;

import AnimFireChalAgent.AnimFireChalAgentGrpc.AnimFireChalAgentImplBase;
import AnimFireChalAgent.AnimFireChalProto.Action;
import AnimFireChalAgent.AnimFireChalProto.ActionInfo;
import AnimFireChalAgent.AnimFireChalProto.Agent;
import AnimFireChalAgent.AnimFireChalProto.AgentInfo;
import io.grpc.stub.StreamObserver;

public class AnimFireChalAgent extends AnimFireChalAgentImplBase {

	@Override
	public void getAgentInfo(ActionInfo request, StreamObserver<AgentInfo> responseObserver) {
		Action[] actions = request.getActionsList().toArray(new Action[0]);
		ActionBean[] actionDetails = new ActionBean[actions.length];
		for (int i =0; i<actions.length; i++) {
			actionDetails[i] = new ActionBean(actions[i].getAgentId(),actions[i].getBuildingId());
		}
//		System.out.println("Action details-------------------");
//		System.out.println(actionDetails.toString());
		AgentResources.setActions(actionDetails);
		
		AgentInfo.Builder resp = AgentInfo.newBuilder();
		
		AgentBean[] agents2 = AgentResources.getAgents();
		for(int i=0; i<agents2.length; i++) {
			Agent a = Agent.newBuilder().setAgentId(agents2[i].getAgent_id()).setX(agents2[i].getX()).setY(agents2[i].getY()).setWater(agents2[i].getWater()).setHp(agents2[i].getHp()).setIdle(1).build();
			resp.addAgents(a);
		}
		
		responseObserver.onNext(resp.build());
		responseObserver.onCompleted();
	}

}
