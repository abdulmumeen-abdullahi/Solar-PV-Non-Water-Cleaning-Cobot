# Import the needed libraries and packages 

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    ur_type = LaunchConfiguration('ur_type')

    urdf_path = PathJoinSubstitution([
        FindPackageShare('husky_ur5_cleaner'), 'urdf', 'huskyur5.urdf.xacro'
    ])

    robot_description = ParameterValue(           # WRAP WITH ParameterValue
        Command([
            FindExecutable(name='xacro'), ' ',
            urdf_path, ' ',
            'ur_type:=', ur_type
        ]),
        value_type=str                            # FORCE STRING TYPE
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'ur_type',
            default_value='ur5',
            description='UR robot type: ur3, ur5, ur10, ur16'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': False
            }],
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('husky_ur5_cleaner'), 'rviz', 'view.rviz'
            ])],
            parameters=[{'use_sim_time': False}]
        ),

    ])