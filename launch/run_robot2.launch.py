import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():

    share_dir = get_package_share_directory('lio_sam')

    parameter_file = LaunchConfiguration('params_file')

    rviz_config_file = os.path.join(
        share_dir,
        'config',
        'rviz',
        'rviz2_robot2.rviz'
    )

    params_declare = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(
            share_dir,
            'config',
            'params_robot2.yaml'
        ),
        description='Path to the ROS2 parameters file to use.'
    )

    tf_remappings = [
        ('/tf', '/robot2/tf'),
        ('/tf_static', '/robot2/tf_static'),
    ]

    return LaunchDescription([

        params_declare,

        Node(
            package='lio_sam',
            executable='lio_sam_imuPreintegration',
            namespace='robot2',
            name='lio_sam_imuPreintegration',
            parameters=[parameter_file],
            remappings=tf_remappings,
            output='screen'
        ),

        Node(
            package='lio_sam',
            executable='lio_sam_imageProjection',
            namespace='robot2',
            name='lio_sam_imageProjection',
            parameters=[parameter_file],
            remappings=tf_remappings,
            output='screen'
        ),

        Node(
            package='lio_sam',
            executable='lio_sam_featureExtraction',
            namespace='robot2',
            name='lio_sam_featureExtraction',
            parameters=[parameter_file],
            remappings=tf_remappings,
            output='screen'
        ),

        Node(
            package='lio_sam',
            executable='lio_sam_mapOptimization',
            namespace='robot2',
            name='lio_sam_mapOptimization',
            parameters=[parameter_file],
            remappings=[
                *tf_remappings,
                (
                    '/lio_sam/mapping/loop_closure_constraints',
                    '/robot2/lio_sam/mapping/loop_closure_constraints'
                ),
            ],
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d',
                rviz_config_file
            ],
            parameters=[
                {'use_sim_time': True}
            ],
            remappings=tf_remappings,
            output='screen'
        )
    ])