
import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


from launch.actions import TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    # Path Definitions
    pkg_name = 'husky_ur5_cleaner'
    pkg_share = get_package_share_directory(pkg_name)
    
    pkg_install_base = get_package_prefix(pkg_name)
    install_share_dir = os.path.join(pkg_install_base, 'share')
    
    world_file = os.path.join(pkg_share, 'worlds', 'solar_farm.sdf')
    xacro_file = os.path.join(pkg_share, 'urdf', 'huskyur5.urdf.xacro')

    # 2. ENVIRONMENT FIX
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.environ.get('GZ_SIM_RESOURCE_PATH', ''),
            ':', install_share_dir,
            ':', os.path.join(pkg_share, 'worlds'),
            ':', os.path.join(pkg_share, 'meshes')
        ]
    )

    # ROBOT STATE PUBLISHER with ParameterValue
    robot_description_content = Command(['xacro ', xacro_file])
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            # Wrap the content in ParameterValue
            'robot_description': ParameterValue(robot_description_content, value_type=str),
            'use_sim_time': True
        }]
    )

    # GAZEBO SIM ENGINE
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch', 'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    # SPAWNER
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'husky_ur5_cobot',
            '-topic', 'robot_description',
            '-z', '0.2'
        ],
        output='screen',
    )


    # ###### 

    # Spawns after 5s to let Gazebo and controller_manager start
    spawn_jsb = TimerAction(period=5.0, actions=[
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
            output='screen',
        )
    ])

    spawn_ur5_ctrl = TimerAction(period=7.0, actions=[
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['ur5_joint_trajectory_controller', '--controller-manager', '/controller_manager'],
            output='screen',
        )
    ])

    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Clock: Gazebo → ROS
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            # Drive commands: ROS → Gazebo
            '/model/husky_ur5_cobot/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            # Odometry: Gazebo → ROS
            '/model/husky_ur5_cobot/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            # Joint states: Gazebo → ROS (needed for robot_state_publisher TF)
            '/model/husky_ur5_cobot/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            # TF from diff drive: Gazebo → ROS
            '/model/husky_ur5_cobot/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ],
        remappings=[
            # Remap Gazebo joint states to the standard /joint_states topic
            ('/model/husky_ur5_cobot/joint_states', '/joint_states'),
            # Remap Gazebo TF to standard /tf
            ('/model/husky_ur5_cobot/tf', '/tf'),
        ],
        output='screen',
    )

    return LaunchDescription([
        set_gz_resource_path,
        node_robot_state_publisher,
        gz_sim,
        spawn_robot,
        spawn_jsb,
        spawn_ur5_ctrl,
        gz_bridge
    ])