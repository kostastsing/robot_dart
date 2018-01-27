#!/usr/bin/env python
# encoding: utf-8
import sys
import glob
sys.path.insert(0, sys.path[0]+'/waf_tools')

VERSION = '0.0.1'
APPNAME = 'robot_dart'

srcdir = '.'
blddir = 'build'

from waflib.Build import BuildContext
import dart
import boost
import eigen


def options(opt):
    opt.load('compiler_cxx')
    opt.load('compiler_c')
    opt.load('boost')
    opt.load('eigen')
    opt.load('dart')


def configure(conf):
    conf.get_env()['BUILD_GRAPHIC'] = False

    conf.load('compiler_cxx')
    conf.load('compiler_c')
    conf.load('boost')
    conf.load('eigen')
    conf.load('dart')

    conf.check_boost(lib='regex system filesystem', min_version='1.46')
    conf.check_eigen()
    conf.check_dart()

    if conf.env.CXX_NAME in ["icc", "icpc"]:
        common_flags = "-Wall -std=c++11"
        opt_flags = " -O3 -xHost  -march=native -mtune=native -unroll -fma -g"
    elif conf.env.CXX_NAME in ["clang"]:
        common_flags = "-Wall -std=c++11"
        opt_flags = " -O3 -march=native -g"
    else:
        if int(conf.env['CC_VERSION'][0]+conf.env['CC_VERSION'][1]) < 47:
            common_flags = "-Wall -std=c++0x"
        else:
            common_flags = "-Wall -std=c++11"
        opt_flags = " -O3 -march=native -g"

    all_flags = common_flags + opt_flags
    conf.env['CXXFLAGS'] = conf.env['CXXFLAGS'] + all_flags.split(' ')
    print conf.env['CXXFLAGS']


def build(bld):

    files = glob.glob(bld.path.abspath()+"/include/robot_dart/*.cpp")
    files = [f[len(bld.path.abspath())+1:] for f in files]
    robot_dart_srcs = " ".join(files)

    bld.stlib(features = 'cxx',
                source = robot_dart_srcs,
                includes = './include',
                uselib = 'BOOST BOOST_SYSTEM BOOST_FILESYSTEM BOOST_REGEX EIGEN DART',
                target = 'robot_dart_simu')

    if bld.get_env()['BUILD_GRAPHIC'] == True:
        bld.program(features = 'cxx',
                      install_path = None,
                      source = 'src/pendulum_test.cpp',
                      includes = './include',
                      uselib = 'BOOST BOOST_SYSTEM BOOST_FILESYSTEM BOOST_REGEX EIGEN DART_GRAPHIC',
                      use = 'robot_dart_simu',
                      defines = ['GRAPHIC'],
                      target = 'pendulum_test')

        bld.program(features = 'cxx',
                      install_path = None,
                      source = 'src/arm_test.cpp',
                      includes = './include',
                      uselib = 'BOOST BOOST_SYSTEM BOOST_FILESYSTEM BOOST_REGEX EIGEN DART_GRAPHIC',
                      use = 'robot_dart_simu',
                      defines = ['GRAPHIC'],
                      target = 'arm_test')

    bld.program(features = 'cxx',
                  install_path = None,
                  source = 'src/pendulum_test.cpp',
                  includes = './include',
                  uselib = 'BOOST BOOST_SYSTEM BOOST_FILESYSTEM BOOST_REGEX DART EIGEN',
                  use = 'robot_dart_simu',
                  target = 'pendulum_test_plain')

    bld.program(features = 'cxx',
                  install_path = None,
                  source = 'src/arm_test.cpp',
                  includes = './include',
                  uselib = 'BOOST BOOST_SYSTEM BOOST_FILESYSTEM BOOST_REGEX DART EIGEN',
                  use = 'robot_dart_simu',
                  target = 'arm_test_plain')

    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/robot_dart_simu.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/robot.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/robot_control.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/simple_control.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/pd_control.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/descriptors.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/macros.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/no_graphics.hpp')
    bld.install_files('${PREFIX}/include/robot_dart', 'include/robot_dart/graphics.hpp')
    bld.install_files('${PREFIX}/share/arm_models/URDF', 'res/models/arm.urdf')
