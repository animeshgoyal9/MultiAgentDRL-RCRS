package AnimFireChalAgent;

public class AgentResources {
	static ActionBean actions[] = new ActionBean[1];
	static AgentBean agents[] = new AgentBean[1];
	
	public static ActionBean[] getActions() {
		return actions;
	}
	public static void setActions(ActionBean[] actions) {
		AgentResources.actions = actions;
	}
	public static AgentBean[] getAgents() {
		return agents;
	}
	public static void setAgents(AgentBean[] agents) {
		AgentResources.agents = agents;
	}
}
