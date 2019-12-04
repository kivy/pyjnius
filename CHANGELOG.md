# Change Log

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



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
