package AnimFireChalAgent;

public class AgentBean {
	int agent_id;
	double x;
	double y;
	int water;
	int hp;
	
	
	public AgentBean() {
		
	}
	public AgentBean(int agent_id, double x, double y, int water, int hp) {
		
		this.agent_id = agent_id;
		this.x = x;
		this.y = y;
		this.water = water;
		this.hp = hp;
	}
	
	public int getAgent_id() {
		return agent_id;
	}
	public void setAgent_id(int agent_id) {
		this.agent_id = agent_id;
	}
	public double getX() {
		return x;
	}
	public void setX(double x) {
		this.x = x;
	}
	public double getY() {
		return y;
	}
	public void setY(double y) {
		this.y = y;
	}
	public int getWater() {
		return water;
	}
	public void setWater(int water) {
		this.water = water;
	}
	public int getHp() {
		return hp;
	}
	public void setHp(int hp) {
		this.hp = hp;
	}
	@Override
	public String toString() {
		return "AgentBean [agent_id=" + agent_id + ", x=" + x + ", y=" + y + ", water=" + water + ", hp=" + hp + "]";
	}
}
