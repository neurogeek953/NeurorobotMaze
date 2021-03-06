
"""
Created on Thu Apr 19 19:02:10 2018
"""

__author__ = 'HBP'

import smach_ros
import smach
from smach import StateMachine
from hbp_nrp_excontrol.nrp_states import WaitToClockState, RobotPoseMonitorState, \
    SetMaterialColorServiceState
from gazebo_msgs.srv import SetLightProperties, GetLightProperties, SetLightPropertiesRequest
from std_msgs.msg import ColorRGBA
from smach import CBState
from hbp_nrp_excontrol.logs import clientLogger

class SetLightProperyState(smach_ros.ServiceState):
    """
    This state sets the light propery
    """
    
    def __init__(self, light, color, attenuation_constant, attenuation_linear, attenuation_quadratic):
        """
        Creates a new service state to set the light

        :param name: The name of the light source that shall be triggered
        :param diffuse: The diffuse of the light.
        :param attenuation_constant: The constant attenuation.
        :param attenuation_linear: The linear attenuation.
        :param attenuation_quadratic: The quadratic attenuation.
        """
        super(SetLightProperyState, self).__init__('/gazebo/set_light_properties',
                                                           SetLightProperties,
                                                           request=SetLightPropertiesRequest(
                                                               light,
                                                               color,
                                                               attenuation_constant,
                                                               attenuation_linear,
                                                               attenuation_quadratic
                                                           ))

sm = StateMachine(outcomes=[FINISHED, ERROR, PREEMPTED])

hotspots = [lambda ud, p: not ((6.2 < p.position.x < 8.0) and (-4.0 < p.position.y < -1.3)),
            lambda ud, p: not ((5.8 < p.position.x < 8.0) and (4.0 < p.position.y < 6.0)),
            lambda ud, p: not ((-0.29 < p.position.x < 0.36879 ) and (3.15 < p.position.y < 6.0)),
            lambda ud, p: not ((-2 < p.position.x < 1) and (-0.44192 < p.position.y < 0.79615)),
            lambda ud, p: not ((-6.69517 < p.position.x <-5.09197) and (-1.25467 < p.position.y < 0.67082)),
            lambda ud, p: not ((-7.05016 < p.position.x <-4.26138) and (-5.60488 < p.position.y < -4.69988)),
            lambda ud, p: not ((0.18991 < p.position.x <1.1271) and (-6.30064 < p.position.y < -4.69988))]

def notify_user_cb(msg):
    @smach.cb_interface(input_keys=[], output_keys=[], outcomes=['finished'])
    def notify_user(userdata):
        clientLogger.advertise(msg)
        return 'finished'
    return notify_user

with sm:

    StateMachine.add(
        "initial_timeline_condition",
        WaitToClockState(5),
        transitions = {'valid': 'initial_timeline_condition',
                       'invalid': 'initial_message',
                       'preempted': PREEMPTED}
    )
    
    StateMachine.add(
            'initial_message',
            CBState(notify_user_cb("In this demo, the husky will try to escape a labyrinth by following the red lights...")),
            transitions = {'finished': 'set_light_red_0'}
    )

    for i in range(len(hotspots)):

        istr = str(i)

        StateMachine.add(
            "set_light_red_"+istr,
            SetLightProperyState('spotlight_'+istr,ColorRGBA(1.0, 0.0, 0.0, 1.0),0.8,0.01,0.001),
            transitions = {'succeeded': 'set_screen_red_'+istr,
                        'aborted': ERROR,
                        'preempted': PREEMPTED}
        )

        StateMachine.add("set_screen_red_"+istr,
            SetMaterialColorServiceState('future_lamp_'+istr,
                                                'future_lamp::body',
                                                'screen_glass',
                                                'Gazebo/RedGlow'),
            transitions = {'succeeded': 'wait_for_husky_screen_'+istr,
                        'aborted': ERROR,
                        'preempted': PREEMPTED}
        )

        StateMachine.add(
             "wait_for_husky_screen_"+istr,
             RobotPoseMonitorState(hotspots[i]),
             transitions = {'valid': 'wait_for_husky_screen_'+istr,
                         'invalid': 'set_screen_blue_'+istr,
                         'preempted': PREEMPTED}
        )
        
        StateMachine.add(
            "set_screen_blue_"+istr,
            SetMaterialColorServiceState('future_lamp_'+istr,
                                                'future_lamp::body',
                                                'screen_glass',
                                                'Gazebo/BlueGlow'),
            transitions = {'succeeded': 'set_light_blue_'+istr,
                        'aborted': ERROR,
                        'preempted': PREEMPTED}
        )

        if i>=len(hotspots)-1:

            StateMachine.add(
                "set_light_blue_"+istr,
                SetLightProperyState('spotlight_'+istr,ColorRGBA(0.0, 0.0, 1.0, 1.0),0.8,0.01,0.001),
                transitions = {'succeeded': "set_screen_red_end",
                            'aborted': ERROR,
                            'preempted': PREEMPTED}
            )

StateMachine.add(
                "set_screen_red_end",
                SetMaterialColorServiceState('future_lamp_'+str(i+1),
                                                    'future_lamp::body',
                                                    'screen_glass',
                                                    'Gazebo/RedGlow'),
                transitions = {'succeeded': "set_light_red_end",
                            'aborted': ERROR,
                            'preempted': PREEMPTED}
            )

            StateMachine.add(
                "set_light_red_end",
                SetLightProperyState('spotlight_'+str(i+1),ColorRGBA(1.0, 0.0, 0.0, 1.0),0.8,0.01,0.001),
                transitions = {'succeeded': 'wait_for_husky_end',
                                  'aborted': ERROR,
                                'preempted': PREEMPTED}
            )

StateMachine.add(
                "wait_for_husky_end",
                RobotPoseMonitorState(lambda ud, p: not ((-1.5 < p.position.x < 1.5) and (-14 < p.position.y < -9.58598))),
                transitions = {'valid': 'wait_for_husky_end',
                            'invalid': 'terminate_demo',
                            'preempted': PREEMPTED}
            )

            StateMachine.add(
                    'terminate_demo',
                    CBState(notify_user_cb("The husky reached its destination!")),
                    transitions = {'finished': FINISHED}
                )

        else:
            StateMachine.add(
                "set_light_blue_"+istr,
                SetLightProperyState('spotlight_'+istr,ColorRGBA(0.0, 0.0, 1.0, 1.0),0.8,0.01,0.001),
                transitions = {'succeeded': "set_light_red_"+str(i+1),
                       'aborted': ERROR,
                            'preempted': PREEMPTED}
            )

