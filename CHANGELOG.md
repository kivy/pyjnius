# Change Log

# [1.6.1](https://github.com/kivy/pyjnius/tree/1.6.1) (2023-11-05)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.6.0...1.6.1)

**Implemented enhancements:**
- [\#684](https://github.com/kivy/pyjnius/pull/684) Add (now mandatory) `.readthedocs.yaml` file, add docs extras and update sphinx conf
- [\#691](https://github.com/kivy/pyjnius/pull/691) Cleanup some Java code in NativeInvocationHandler.java
- [\#692](https://github.com/kivy/pyjnius/pull/692) Skip getting version from `Cython` on Android. Instead add `ANDROID_PYJNUS_CYTHON_3` env var
- [\#693](https://gtihub.com/kivy/pyjnius/pull/693) Use the `release/v1` tag for `pypa/gh-action-pypi-publish`, as `master` is deprecated

# [1.6.0](https://github.com/kivy/pyjnius/tree/1.6.0) (2023-10-07)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.5.0...1.6.0)

**Implemented enhancements:**
- [\#659](https://github.com/kivy/pyjnius/pull/659) introduce protocol_map for Map$Entry
- [\#669](https://github.com/kivy/pyjnius/pull/669) Support both Cython >3 and Cython < 3
- [\#672](https://github.com/kivy/pyjnius/pull/672) Support Java 20, remove Java 7 support
- [\#673](https://github.com/kivy/pyjnius/pull/673) Remove pkg_resources for Python >=3.9
- [\#681](https://github.com/kivy/pyjnius/pull/681) Add missing Python supported version label for Python 3.12

**Packaging**
- [\#680](https://github.com/kivy/pyjnius/pull/680) Update cibuildwheel to perform build for Python 3.12

**CI**
- [\#676](https://github.com/kivy/pyjnius/pull/676) Ensure we test the produced wheel, and not the one from the index
- [\#678](https://github.com/kivy/pyjnius/pull/678) Add tests for python 3.12
- [\#677](https://github.com/kivy/pyjnius/pull/677) Now Github Actions provides python3 via setup-python also for Apple Silicon Macs
- [\#679](https://github.com/kivy/pyjnius/pull/679) Add tests on push for Apple Silicon
- [\#682](https://github.com/kivy/pyjnius/pull/682) Build stdist needs Cython to perform the build


## [1.5.0](https://github.com/kivy/pyjnius/tree/1.5.0) (2023-05-10)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.4.2...1.5.0)

**Implemented enhancements:**
- [\#633](https://github.com/kivy/pyjnius/pull/633) Add BSD Unix build support (FreeBSD, OpenBSD, NetBSD, ..)
- [\#643](https://github.com/kivy/pyjnius/pull/643) Initialize logger as a child of the Kivy's one
- [\#657](https://github.com/kivy/pyjnius/pull/657) Add support request automation (as other kivy projects)
- [\#656](https://github.com/kivy/pyjnius/pull/656) Add support for Python 3.11

**Cleanup**
- [\#619](https://github.com/kivy/pyjnius/pull/619) Remove Python 2 support, six dependency
- [\#641](https://github.com/kivy/pyjnius/pull/641) Removes some Python2-era complexity
- [\#654](https://github.com/kivy/pyjnius/pull/654) Remove Python 3.6 from supported and test matrix, as it reached EOL

**CI**
- [\#655](https://github.com/kivy/pyjnius/pull/655) Linux x86 tests force as safe directory

**Packaging**
- [\#653](https://github.com/kivy/pyjnius/pull/653) Build (and test) `manylinux-aarch64` wheels via our `kivy-ubuntu-arm64` self-hosted runner


## [1.4.2](https://github.com/kivy/pyjnius/tree/1.4.2) (2022-07-02)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.4.1...1.4.2)

**CI**
- [\#628](https://github.com/kivy/pyjnius/pull/628) Updated java-setup to v3, include all the LTS versions from adoptium during CI tests.

**Packaging**
- [\#620](https://github.com/kivy/pyjnius/pull/620) When cross-compiling for Android, we should not use the include dirs exposed by the JDK
- [\#629](https://github.com/kivy/pyjnius/pull/629) Cython now requires a minimum version. Introduces setup.cfg. Cleans up the CI workflow
- [\#625](https://github.com/kivy/pyjnius/pull/625) Use cibuildwheel for releases

**Docs**
- [\#616](https://github.com/kivy/pyjnius/pull/616) Update api.rst, remove extra equals signs

**Implemented enhancements:**
- [\#622](https://github.com/kivy/pyjnius/pull/622) Add suffix to support IBM jre on Windows
- [\#626](https://github.com/kivy/pyjnius/pull/626) Move get_cpu guessing into _possible_lib_location
- [\#627](https://github.com/kivy/pyjnius/pull/627) PyPy: Fixes a segfault + add tests

## [1.4.1](https://github.com/kivy/pyjnius/tree/1.4.1) (2021-10-30)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.4.0...1.4.1)

**CI**
- [\#607](https://github.com/kivy/pyjnius/pull/607) Add python3.10 build/release

**Packaging**
- [\#603](https://github.com/kivy/pyjnius/pull/603) Use platform.machine() as default get_cpu() return value, explicitely support AARCH64


## [1.4.0](https://github.com/kivy/pyjnius/tree/1.4.0) (2021-08-24)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.3.0...1.4.0)

**Implemented enhancements:**
- [\#542](https://github.com/kivy/pyjnius/pull/542) Improve performance of byte array parameters
- [\#515](https://github.com/kivy/pyjnius/pull/515) Allow passing Python Lambdas as Java lambdas
- [\#541](https://github.com/kivy/pyjnius/pull/541) Refactor of env.py

**Fixed bugs:**
- [\#549](https://github.com/kivy/pyjnius/pull/549) Fixes #548 JVM options are not correctly set by jnius_config.set_options()
- [\#546](https://github.com/kivy/pyjnius/pull/546) Add in missing assignable check for int parameters etc.
- [\#558](https://github.com/kivy/pyjnius/pull/558) Improve error message on method not found
- [\#567](https://github.com/kivy/pyjnius/pull/567) Fix static methods
- [\#566](https://github.com/kivy/pyjnius/pull/566) fix bug for constuctors with variable arguments
- [\#569](https://github.com/kivy/pyjnius/pull/569) set_resolve_info: replace j_self w/ resolve_static
- [\#595](https://github.com/kivy/pyjnius/pull/595) Use Python standard library `which` instead of OS `which`

**Documentation**
- [\#556](https://github.com/kivy/pyjnius/pull/556) fix link in readme
- [\#572](https://github.com/kivy/pyjnius/pull/572) update readme for python3
- [\#584](https://github.com/kivy/pyjnius/pull/584) Updated android.rst for python3
- [\#565](https://github.com/kivy/pyjnius/pull/565) Update python versions

**CI**
- [\#560](https://github.com/kivy/pyjnius/pull/560) added x86 workflow
- [\#564](https://github.com/kivy/pyjnius/pull/564) run on pull request & add missing badge
- [\#536](https://github.com/kivy/pyjnius/pull/536) add missing architecture for python setup in actions

**Packaging**
- [\#594](https://github.com/kivy/pyjnius/pull/594) Add pyproject.toml to specify Cython as a build requirement

## [1.3.0](https://github.com/kivy/pyjnius/tree/1.3.0) (2020-05-03)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.2.1...1.3.0)

**Implemented enhancements:**
- [\#483](https://github.com/kivy/pyjnius/pull/483)/[\#489](https://github.com/kivy/pyjnius/pull/489) allow passing a `signature` argument to constructors, to force selection of the desired one
- [\#497](https://github.com/kivy/pyjnius/pull/497)/[\#506](https://github.com/kivy/pyjnius/pull/506)/[\#507](https://github.com/kivy/pyjnius/pull/507) support for more "dunder" methods/protocols on compatible interfaces than just `__len__`, and allow users to provide their own.
- [\#500](https://github.com/kivy/pyjnius/pull/500)[\#522](https://github.com/kivy/pyjnius/pull/522) allow ignoring private methods and fields in autoclass (both default to False)
- [\#503](https://github.com/kivy/pyjnius/pull/503) auto detect java_home on OSX, using `/usr/libexec/java_home` (if JAVA_HOME is not declared)
- [\#514](https://github.com/kivy/pyjnius/pull/514) writing to static fields (and fix reading from them)
- [\#517](https://github.com/kivy/pyjnius/pull/517) make signature exceptions more useful
- [\#502](https://github.com/kivy/pyjnius/pull/502) provide a stacktrace for where JVM was started.
- [\#523](https://github.com/kivy/pyjnius/pull/523) expose the class's class attribute
- [\#524](https://github.com/kivy/pyjnius/pull/524) fix handling of Java chars > 256 in Python3
- [\#519](https://github.com/kivy/pyjnius/pull/519) Always show the exception name

**Fixed bugs:**
- [\#481](https://github.com/kivy/pyjnius/pull/481) wrong use of strip on JRE path
- [\#465](https://github.com/kivy/pyjnius/pull/465) correct reflection to avoid missing any methods from parent classes or interfaces
- [\#508](https://github.com/kivy/pyjnius/pull/508) don't had error details with a custom exception when java class is not found
- [\#510](https://github.com/kivy/pyjnius/pull/510) add missing references to .pxi files in setup.py, speeding up recompilation
- [\#518](https://github.com/kivy/pyjnius/pull/518) ensure autoclass prefers methods over properties
- [\#520](https://github.com/kivy/pyjnius/pull/520) improved discovery of libjvm.so + provide a workaround if it doesn't work

**Documentation**
- [\#478](https://github.com/kivy/pyjnius/pull/478) document automatic Thread detach feature
- [\#512](https://github.com/kivy/pyjnius/pull/512) document the requirement to keep reference to object/functions passed to java, for as long as it might use them
- [\#521](https://github.com/kivy/pyjnius/pull/521) fix inheritance in example


## [1.2.1](https://github.com/kivy/pyjnius/tree/1.2.1) (2019-12-04)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.2.0...1.2.1)

- Make sure methods are discovered in reverse-inheritance order
- fix unreferenced variable
- Avoid windows execution error when JAVA_HOME path has space (test on w10)
- Link to libjli, not libjvm, on macOS
- Add support for adoptopenjdk12
- Add build support for Oracle Solaris on SPARC sun4u and sun4v
- make sure Interface have access to Object's methods
- wheels built for:
  - Windows: Python 3.6, 3.7 and 3.8
  - OSX: Python 2.7, 3.6, 3.7 and 3.8
  - Manylinux: Python 2.7, 3.6, 3.7 and 3.8

## [1.2.0](https://github.com/kivy/pyjnius/tree/1.2.0) (2019-02-04)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.1.4...1.2.0)

## [1.1.4](https://github.com/kivy/pyjnius/tree/1.1.4) (2018-12-05)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.1.3...1.1.4)

## [1.1.3](https://github.com/kivy/pyjnius/tree/1.1.3) (2018-10-22)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.1.2...1.1.3)

## [1.1.2](https://github.com/kivy/pyjnius/tree/1.1.2) (2018-10-17)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.1.1...1.1.2)

## [1.1.1](https://github.com/kivy/pyjnius/tree/1.1.1) (2017-03-24)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.1.0...1.1.1)

**Implemented enhancements:**

- Rename jnius to pyjnius for pypi [\#266](https://github.com/kivy/pyjnius/issues/266)

## [1.1.0](https://github.com/kivy/pyjnius/tree/1.1.0) (2017-03-23)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.0.3...1.1.0)

**Implemented enhancements:**

- Java Iterables [\#45](https://github.com/kivy/pyjnius/issues/45)
- API for human-readable method signatures [\#133](https://github.com/kivy/pyjnius/pull/133) ([chrisjrn](https://github.com/chrisjrn))

**Fixed bugs:**

- import jnius on Centos7/python 3.4: AttributeError: 'str' object has no attribute 'decode' [\#218](https://github.com/kivy/pyjnius/issues/218)
- ByteArray values over 127 \(0x7f\) causes OverFlow error [\#93](https://github.com/kivy/pyjnius/issues/93)
- Leak in Runnable [\#83](https://github.com/kivy/pyjnius/issues/83)
- Output parameters don't works [\#58](https://github.com/kivy/pyjnius/issues/58)
- Apache Error: child pid XXXXX exit signal Segmentation fault \(11\) [\#50](https://github.com/kivy/pyjnius/issues/50)
- pyjnius is not thread-safe [\#46](https://github.com/kivy/pyjnius/issues/46)
- Problem on 64 bit ubuntu 12.04 [\#18](https://github.com/kivy/pyjnius/issues/18)
- In file included from jnius/jnius.c:4:0:     /usr/include/python2.7/Python.h:22:2: error: \#error "Something's broken.  UCHAR\_MAX should be defined in limits.h." [\#11](https://github.com/kivy/pyjnius/issues/11)
- doesn't work on windows [\#9](https://github.com/kivy/pyjnius/issues/9)
- varargs don’t seem to work [\#8](https://github.com/kivy/pyjnius/issues/8)
- setup.py  jre\_home [\#1](https://github.com/kivy/pyjnius/issues/1)

**Closed issues:**

- How to import the kivy's activity? [\#258](https://github.com/kivy/pyjnius/issues/258)
- shouldOverrideUrlLoading webview android [\#250](https://github.com/kivy/pyjnius/issues/250)
- App crashes if we use 'org.renpy.android.PythonActivity' in p4a new toolchain [\#249](https://github.com/kivy/pyjnius/issues/249)
- missing import os in jnius/\_\_init\_\_.py - there should be a CI workflow for pyjnius [\#245](https://github.com/kivy/pyjnius/issues/245)
- jnius.detach\(\) not safe with  local variables [\#240](https://github.com/kivy/pyjnius/issues/240)
- Type casting is not implemented [\#229](https://github.com/kivy/pyjnius/issues/229)
- Pyjnius doesn't compile with cython 0.24 [\#219](https://github.com/kivy/pyjnius/issues/219)
- jnius\jnius.c\(4205\) : error C2065: 'const\_char' : undeclared identifier ,install on windows [\#214](https://github.com/kivy/pyjnius/issues/214)
- pyjnius not working in virtual environment  [\#213](https://github.com/kivy/pyjnius/issues/213)
- Getting JAVA\_HOME KeyError while importing autoclass [\#209](https://github.com/kivy/pyjnius/issues/209)
- Not able to install pyjnius on windows 7 and python 3.4. Error: jnius.obj lnk 2019 [\#206](https://github.com/kivy/pyjnius/issues/206)
- \_\_javaclass\_\_ definition missing  [\#193](https://github.com/kivy/pyjnius/issues/193)
- unexpeted output cjtp:r [\#190](https://github.com/kivy/pyjnius/issues/190)
- can't import Contacts [\#180](https://github.com/kivy/pyjnius/issues/180)
- compilation error in master after ~3.11.2015 [\#178](https://github.com/kivy/pyjnius/issues/178)
- AttributeError: 'str' object has no attribute 'decode' [\#176](https://github.com/kivy/pyjnius/issues/176)
- AttributeError: type object 'android.widget.AbsoluteLayout' has no attribute 'LayoutParams' [\#175](https://github.com/kivy/pyjnius/issues/175)
- Lib should work with python3 [\#165](https://github.com/kivy/pyjnius/issues/165)
- make tests never passes [\#162](https://github.com/kivy/pyjnius/issues/162)
- Can't make an EnumMap? [\#159](https://github.com/kivy/pyjnius/issues/159)
- Release to PyPI? [\#156](https://github.com/kivy/pyjnius/issues/156)
- OverflowError: Python int too large to convert to C long on ART [\#146](https://github.com/kivy/pyjnius/issues/146)
- Misunderstood [\#141](https://github.com/kivy/pyjnius/issues/141)
- License is MIT but setup.py still says LGPL [\#139](https://github.com/kivy/pyjnius/issues/139)
- Segmentation fault occurs in wrapped C lib, only when jnius is imported [\#136](https://github.com/kivy/pyjnius/issues/136)
- Failing build\_ext target with Cython 0.21 [\#131](https://github.com/kivy/pyjnius/issues/131)
- Cannot create AdRequest instance [\#124](https://github.com/kivy/pyjnius/issues/124)
- Native invocation issue with ART [\#113](https://github.com/kivy/pyjnius/issues/113)
- pyjnius custom classpath exception [\#109](https://github.com/kivy/pyjnius/issues/109)
-  some reports from users complaining about "native thread exited without detaching..." [\#107](https://github.com/kivy/pyjnius/issues/107)
- jnius.JavaException: Class not found [\#106](https://github.com/kivy/pyjnius/issues/106)
- Exception: Invalid "\[" character in definition [\#104](https://github.com/kivy/pyjnius/issues/104)
- Does Pyjinius support Python 3? [\#103](https://github.com/kivy/pyjnius/issues/103)
- Pyjnius: Find own classes on mac 10.9 [\#102](https://github.com/kivy/pyjnius/issues/102)
- java.util.TimeZone not working with python threads [\#97](https://github.com/kivy/pyjnius/issues/97)
- Android/ART crash Invalid instance of… [\#92](https://github.com/kivy/pyjnius/issues/92)
- PyPy / cffi? [\#88](https://github.com/kivy/pyjnius/issues/88)
- Not installing [\#84](https://github.com/kivy/pyjnius/issues/84)
- Accessing fields on multiple instances of same class returns value of last [\#77](https://github.com/kivy/pyjnius/issues/77)
- Win7, python2.7.5 \(32bits\) ... with phyjnius 1.2.1 --\> ImportError: DLL load failed: [\#70](https://github.com/kivy/pyjnius/issues/70)
- lookup\_java\_object\_name leaks LocalRefs [\#68](https://github.com/kivy/pyjnius/issues/68)
- Memory leak in constructor [\#67](https://github.com/kivy/pyjnius/issues/67)
- README accelerometer example code out of date? [\#64](https://github.com/kivy/pyjnius/issues/64)
- How to navigation buttons [\#61](https://github.com/kivy/pyjnius/issues/61)
- JavaException: JVM exception occured [\#60](https://github.com/kivy/pyjnius/issues/60)
- How do I install it? [\#57](https://github.com/kivy/pyjnius/issues/57)
- JavaException: Unable to found the class for 'java/lang/CharSequence'  [\#56](https://github.com/kivy/pyjnius/issues/56)
- Accessing Android's clipboard [\#55](https://github.com/kivy/pyjnius/issues/55)
- \[armhf\] - Builds fail on launchpad [\#53](https://github.com/kivy/pyjnius/issues/53)
- How to run  java class? [\#51](https://github.com/kivy/pyjnius/issues/51)
- Can not find class with www-data account [\#49](https://github.com/kivy/pyjnius/issues/49)
- Compilation Error [\#48](https://github.com/kivy/pyjnius/issues/48)
- Setting JVM options [\#44](https://github.com/kivy/pyjnius/issues/44)
- Tests don't pass \(doesn't find libraries\) [\#43](https://github.com/kivy/pyjnius/issues/43)
- pyjnius does not seems to be installed properly in osx 10.6 [\#39](https://github.com/kivy/pyjnius/issues/39)
- Make it possible to convert a python list to a Java array [\#35](https://github.com/kivy/pyjnius/issues/35)
- Cast python object to a Java Object [\#33](https://github.com/kivy/pyjnius/issues/33)
- Doesn't work under Windows 7 [\#30](https://github.com/kivy/pyjnius/issues/30)
- no multidimensional array support [\#29](https://github.com/kivy/pyjnius/issues/29)
- Create new tag \(1.03?\) [\#28](https://github.com/kivy/pyjnius/issues/28)
- array of bytes [\#27](https://github.com/kivy/pyjnius/issues/27)
- Can't install at Macosx lion [\#23](https://github.com/kivy/pyjnius/issues/23)

**Merged pull requests:**

- Update installation.rst: Instructions for Windows [\#224](https://github.com/kivy/pyjnius/pull/224) ([harishankarv](https://github.com/harishankarv))
- Handle charsequence [\#212](https://github.com/kivy/pyjnius/pull/212) ([akshayaurora](https://github.com/akshayaurora))
- add version to six requirement [\#204](https://github.com/kivy/pyjnius/pull/204) ([kived](https://github.com/kived))
- Updated readme to counter issues \#197 [\#202](https://github.com/kivy/pyjnius/pull/202) ([jk1ng](https://github.com/jk1ng))
- setup fixes for python 3.5 [\#200](https://github.com/kivy/pyjnius/pull/200) ([danielepantaleone](https://github.com/danielepantaleone))
- setup: fixed invalid libjvm.so reference on i386 cpu [\#198](https://github.com/kivy/pyjnius/pull/198) ([danielepantaleone](https://github.com/danielepantaleone))
- Adding support for armhf builds [\#184](https://github.com/kivy/pyjnius/pull/184) ([thopiekar](https://github.com/thopiekar))
- compilation error fixed [\#179](https://github.com/kivy/pyjnius/pull/179) ([ibobalo](https://github.com/ibobalo))
- Followup fixes for python 3 [\#177](https://github.com/kivy/pyjnius/pull/177) ([benson-basis](https://github.com/benson-basis))
- Use the java from java\_home on OSX. [\#166](https://github.com/kivy/pyjnius/pull/166) ([benson-basis](https://github.com/benson-basis))
- Make this work with python 3.4 as well as 2.7 [\#164](https://github.com/kivy/pyjnius/pull/164) ([benson-basis](https://github.com/benson-basis))
- Fix build tests [\#163](https://github.com/kivy/pyjnius/pull/163) ([benson-basis](https://github.com/benson-basis))
- Fix 159: passing the result of autoclass to java.lang.Class parameter. [\#160](https://github.com/kivy/pyjnius/pull/160) ([benson-basis](https://github.com/benson-basis))
- Another missing PR [\#153](https://github.com/kivy/pyjnius/pull/153) ([remram44](https://github.com/remram44))
- Re-applies \#138 [\#152](https://github.com/kivy/pyjnius/pull/152) ([remram44](https://github.com/remram44))
- Enable setting primitive data type fields on Java classes [\#150](https://github.com/kivy/pyjnius/pull/150) ([msmolens](https://github.com/msmolens))
- OS X: use JavaVM framework from current Mac OS SDK [\#149](https://github.com/kivy/pyjnius/pull/149) ([msmolens](https://github.com/msmolens))
- Update jnius\_conversion.pxi [\#144](https://github.com/kivy/pyjnius/pull/144) ([retsyo](https://github.com/retsyo))
- use temporary var to handle unsigned char -\> jbyte \(signed char\) [\#142](https://github.com/kivy/pyjnius/pull/142) ([kived](https://github.com/kived))
- Fix JVM signatures for the java.lang.Class methods. [\#138](https://github.com/kivy/pyjnius/pull/138) ([tonyfinn](https://github.com/tonyfinn))
- Fixed sound recorder example syntax error [\#129](https://github.com/kivy/pyjnius/pull/129) ([prophittcorey](https://github.com/prophittcorey))
- fix print statement [\#128](https://github.com/kivy/pyjnius/pull/128) ([dessant](https://github.com/dessant))
- Update api.rst [\#121](https://github.com/kivy/pyjnius/pull/121) ([JustinCappos](https://github.com/JustinCappos))
- Issue 96 improved exception handling [\#115](https://github.com/kivy/pyjnius/pull/115) ([Lenbok](https://github.com/Lenbok))
- Add support for multidimensional arrays [\#111](https://github.com/kivy/pyjnius/pull/111) ([abrasive](https://github.com/abrasive))
- Add control of JVM startup options [\#110](https://github.com/kivy/pyjnius/pull/110) ([abrasive](https://github.com/abrasive))
- Removes LGPL license in 'COPYING' [\#94](https://github.com/kivy/pyjnius/pull/94) ([remram44](https://github.com/remram44))
- Successfully compiled for Windows [\#87](https://github.com/kivy/pyjnius/pull/87) ([kevlened](https://github.com/kevlened))
- Fix field dereference when multiple instances of a class exist. Fixes \#77 [\#78](https://github.com/kivy/pyjnius/pull/78) ([zielmicha](https://github.com/zielmicha))
- Document autoclass syntax for nested Java classes. [\#74](https://github.com/kivy/pyjnius/pull/74) ([Ian-Foote](https://github.com/Ian-Foote))
- Fix string format error in 2.6 [\#72](https://github.com/kivy/pyjnius/pull/72) ([limodou](https://github.com/limodou))
- fix NotImplemented not found [\#69](https://github.com/kivy/pyjnius/pull/69) ([smglab](https://github.com/smglab))
- Check for exception after calling constructor [\#66](https://github.com/kivy/pyjnius/pull/66) ([zielmicha](https://github.com/zielmicha))
- improve JRE/JDK home detection using which and default JRE location when JDK is installed [\#63](https://github.com/kivy/pyjnius/pull/63) ([ghost](https://github.com/ghost))
- A couple of quick fixes [\#52](https://github.com/kivy/pyjnius/pull/52) ([artagnon](https://github.com/artagnon))
- Updated to support Mac OS X build support [\#42](https://github.com/kivy/pyjnius/pull/42) ([allfro](https://github.com/allfro))
- added support for Python Java class objects as parameter of java methods that takes Java Class object as parameter [\#41](https://github.com/kivy/pyjnius/pull/41) ([ghost](https://github.com/ghost))
- Added basic tests that shows that autoclass of interface, nested enum and nested class is possible  [\#40](https://github.com/kivy/pyjnius/pull/40) ([ghost](https://github.com/ghost))
- Several fixes related to arrays being Java Object [\#37](https://github.com/kivy/pyjnius/pull/37) ([ghost](https://github.com/ghost))
- Method resolutions fixes for the case where there are varargs [\#36](https://github.com/kivy/pyjnius/pull/36) ([ghost](https://github.com/ghost))
- Fixed URI Bug \( uri.parse \) [\#31](https://github.com/kivy/pyjnius/pull/31) ([GeorgS](https://github.com/GeorgS))

## [1.0.3](https://github.com/kivy/pyjnius/tree/1.0.3) (2012-09-06)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.0.2...1.0.3)

**Closed issues:**

- cython error [\#25](https://github.com/kivy/pyjnius/issues/25)
- All modules called jnius\_xxxx.pxi [\#17](https://github.com/kivy/pyjnius/issues/17)

**Merged pull requests:**

- Varargs support [\#26](https://github.com/kivy/pyjnius/pull/26) ([tshirtman](https://github.com/tshirtman))
- Allow for '\*' wildcards in CLASSPATH+\(some tipos\). [\#24](https://github.com/kivy/pyjnius/pull/24) ([apalala](https://github.com/apalala))
- Typo in line 39  [\#20](https://github.com/kivy/pyjnius/pull/20) ([nklever](https://github.com/nklever))
- Make the desktop use CLASSPATH if defined. [\#14](https://github.com/kivy/pyjnius/pull/14) ([apalala](https://github.com/apalala))
- Update README.md [\#10](https://github.com/kivy/pyjnius/pull/10) ([graingert](https://github.com/graingert))

## [1.0.2](https://github.com/kivy/pyjnius/tree/1.0.2) (2012-08-20)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.0.1...1.0.2)

**Closed issues:**

- cython can't find jni.pxi [\#7](https://github.com/kivy/pyjnius/issues/7)

## [1.0.1](https://github.com/kivy/pyjnius/tree/1.0.1) (2012-08-20)
[Full Changelog](https://github.com/kivy/pyjnius/compare/1.0...1.0.1)

**Closed issues:**

- Can't install from PyPi [\#5](https://github.com/kivy/pyjnius/issues/5)

**Merged pull requests:**

- Add cython to install\_requires Fixes \#5 [\#6](https://github.com/kivy/pyjnius/pull/6) ([graingert](https://github.com/graingert))

## [1.0](https://github.com/kivy/pyjnius/tree/1.0) (2012-08-20)
**Closed issues:**

- Sets and ArrayLists not converted to python sets/lists [\#4](https://github.com/kivy/pyjnius/issues/4)
- Java doesn't accept our subclasses as arguments [\#3](https://github.com/kivy/pyjnius/issues/3)

**Merged pull requests:**

- small grammatical changes [\#2](https://github.com/kivy/pyjnius/pull/2) ([dekoza](https://github.com/dekoza))
