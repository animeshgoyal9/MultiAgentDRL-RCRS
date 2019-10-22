# RoboCup RCF Project

The Integration of RoboCup Rescue Agent Simulation to OpenAI Gym

## Design 

We build python API for RoboCup Rescue simulator. 
Basically we aim to rewrite java communication and agent codes in python.
For that purposes we list the java classes and its corresponding python modules

|Java Classes  | Python Modules |
|------------- | -------------- |
|`rescuecore2.connection.TCPConnection`, `rescuecore2.connection.StreamConnection`, `rescuecore2.connection.AbstractConnection`, `rescuecore2.connection.Connect` | `tcp_connection` |
|`rescuecore2.components.AbstractAgent`, `rescuecore2.components.AbstractComponent`, `rescuecore2.components.Component` | `rescue_agent` |
|`rescuecore2.messages.control.ControlMessageFactory`, `rescuecore2.messages.control.StandardMessageFactory` | `message_factory` |
|`rescuecore2.messages.component.*` | `message_component` |
|`rescuecore2.messages.control.*` | `message` |
|`rescuecore2.misc.EncodingTools` | `encoding_tool` |
|`sample.LaunchSampleAgents` | `agent_launcher` |
|`rescuecore2.worldmodel.ChangeSet`|`change_set`|
|`rescuecore2.worldmodel.Entity`,`rescuecore2.worldmodel.EntityID`,
`rescuecore2.worldmodel.Property`|`world_model`|
|`rescuecore2.registry.Registry`|`registry`|
|`rescuecore2.config.*`|`config`|
-------------------------------------------------

## Testing

To run the rescue server with test map, you navigate to the boot directory of rescue simulator and run: `./start.sh -c ../maps/gml/test/config/ -m ../maps/gml/test/map/`

To run the python agent module: `python agent_launcher.py -p 7000 -h 127.0.0.1 -fb 1 -pf 0 -at 0` Note that this script connects only a firebrigade agent.

To run the dummy OpenAIGym environment: 
First, we need to run: `python setup.py install`
And then: `python testing.py`
