<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>TheSolutionMainWindow</class>
 <widget class="QMainWindow" name="TheSolutionMainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1400</width>
    <height>900</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>TheSolution CAD - Главное окно</string>
  </property>
  <property name="windowIcon">
   <iconset>
    <normaloff>:/icons/thesolution.png</normaloff>:/icons/thesolution.png</iconset>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QHBoxLayout" name="horizontalLayout">
    <property name="spacing">
     <number>6</number>
    </property>
    <property name="leftMargin">
     <number>6</number>
    </property>
    <property name="topMargin">
     <number>6</number>
    </property>
    <property name="rightMargin">
     <number>6</number>
    </property>
    <property name="bottomMargin">
     <number>6</number>
    </property>
    <item>
     <widget class="QSplitter" name="mainSplitter">
      <property name="orientation">
       <enum>Qt::Horizontal</enum>
      </property>
      <property name="childrenCollapsible">
       <bool>false</bool>
      </property>
      <!-- Левая панель - Дерево объектов -->
      <widget class="QWidget" name="leftPanel" native="true">
       <property name="minimumSize">
        <size>
         <width>250</width>
         <height>0</height>
        </size>
       </property>
       <property name="maximumSize">
        <size>
         <width>400</width>
         <height>16777215</height>
        </size>
       </property>
       <layout class="QVBoxLayout" name="leftPanelLayout">
        <property name="spacing">
         <number>6</number>
        </property>
        <property name="leftMargin">
         <number>6</number>
        </property>
        <property name="topMargin">
         <number>6</number>
        </property>
        <property name="rightMargin">
         <number>6</number>
        </property>
        <property name="bottomMargin">
         <number>6</number>
        </property>
        <!-- Заголовок дерева объектов -->
        <item>
         <widget class="QLabel" name="treeLabel">
          <property name="text">
           <string>Объекты Solution</string>
          </property>
          <property name="font">
           <font>
            <pointsize>10</pointsize>
            <bold>true</bold>
           </font>
          </property>
         </widget>
        </item>
        <!-- Дерево объектов -->
        <item>
         <widget class="QTreeWidget" name="solutionTree">
          <property name="headerHidden">
           <bool>false</bool>
          </property>
          <property name="rootIsDecorated">
           <bool>true</bool>
          </property>
          <property name="uniformRowHeights">
           <bool>false</bool>
          </property>
          <property name="itemsExpandable">
           <bool>true</bool>
          </property>
          <property name="sortingEnabled">
           <bool>false</bool>
          </property>
          <property name="wordWrap">
           <bool>false</bool>
          </property>
          <property name="headerVisible">
           <bool>true</bool>
          </property>
          <column>
           <property name="text">
            <string>Имя</string>
           </property>
          </column>
          <column>
           <property name="text">
            <string>Тип</string>
           </property>
          </column>
          <column>
           <property name="text">
            <string>ID</string>
           </property>
          </column>
         </widget>
        </item>
        <!-- Кнопки управления объектами -->
        <item>
         <widget class="QGroupBox" name="objectControlsGroup">
          <property name="title">
           <string>Управление объектами</string>
          </property>
          <layout class="QGridLayout" name="objectControlsLayout">
           <item row="0" column="0">
            <widget class="QPushButton" name="createBoxButton">
             <property name="text">
              <string>Создать куб</string>
             </property>
             <property name="icon">
              <iconset>
               <normaloff>:/icons/cube.png</normaloff>:/icons/cube.png</iconset>
             </property>
            </widget>
           </item>
           <item row="0" column="1">
            <widget class="QPushButton" name="createSphereButton">
             <property name="text">
              <string>Создать сферу</string>
             </property>
             <property name="icon">
              <iconset>
               <normaloff>:/icons/sphere.png</normaloff>:/icons/sphere.png</iconset>
             </property>
            </widget>
           </item>
           <item row="1" column="0">
            <widget class="QPushButton" name="createCylinderButton">
             <property name="text">
              <string>Создать цилиндр</string>
             </property>
             <property name="icon">
              <iconset>
               <normaloff>:/icons/cylinder.png</normaloff>:/icons/cylinder.png</iconset>
             </property>
            </widget>
           </item>
           <item row="1" column="1">
            <widget class="QPushButton" name="createAssemblyButton">
             <property name="text">
              <string>Создать сборку</string>
             </property>
             <property name="icon">
              <iconset>
               <normaloff>:/icons/assembly.png</normaloff>:/icons/assembly.png</iconset>
             </property>
            </widget>
           </item>
           <item row="2" column="0" colspan="2">
            <widget class="QPushButton" name="deleteObjectButton">
             <property name="text">
              <string>Удалить объект</string>
             </property>
             <property name="icon">
              <iconset>
               <normaloff>:/icons/delete.png</normaloff>:/icons/delete.png</iconset>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </item>
       </layout>
      </widget>
      <!-- Центральная панель - 3D вид -->
      <widget class="QWidget" name="centerPanel" native="true">
       <layout class="QVBoxLayout" name="centerPanelLayout">
        <property name="spacing">
         <number>6</number>
        </property>
        <property name="leftMargin">
         <number>6</number>
        </property>
        <property name="topMargin">
         <number>6</number>
        </property>
        <property name="rightMargin">
         <number>6</number>
        </property>
        <property name="bottomMargin">
         <number>6</number>
        </property>
        <!-- Панель инструментов 3D -->
        <item>
         <widget class="QToolBar" name="viewToolBar">
          <property name="windowTitle">
           <string>Панель инструментов 3D</string>
          </property>
          <property name="toolButtonStyle">
           <enum>Qt::ToolButtonIconOnly</enum>
          </property>
          <addaction name="actionZoomIn"/>
          <addaction name="actionZoomOut"/>
          <addaction name="separator"/>
          <addaction name="actionRotate"/>
          <addaction name="actionPan"/>
          <addaction name="actionSelect"/>
          <addaction name="separator"/>
          <addaction name="actionFrontView"/>
          <addaction name="actionTopView"/>
          <addaction name="actionSideView"/>
          <addaction name="actionIsometricView"/>
         </widget>
        </item>
        <!-- 3D вид -->
        <item>
         <widget class="QFrame" name="viewFrame">
          <property name="frameShape">
           <enum>QFrame::StyledPanel</enum>
          </property>
          <property name="frameShadow">
           <enum>QFrame::Raised</enum>
          </property>
          <layout class="QVBoxLayout" name="viewLayout">
           <item>
            <widget class="QWidget" name="openGLWidget" native="true">
             <property name="minimumSize">
              <size>
               <width>600</width>
               <height>400</height>
              </size>
             </property>
             <property name="styleSheet">
              <string notr="true">background-color: #2b2b2b;</string>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </item>
        <!-- Статусная строка 3D -->
        <item>
         <widget class="QStatusBar" name="viewStatusBar">
          <property name="maximumSize">
           <size>
            <width>16777215</width>
            <height>25</height>
           </size>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <!-- Правая панель - Свойства -->
      <widget class="QWidget" name="rightPanel" native="true">
       <property name="minimumSize">
        <size>
         <width>300</width>
         <height>0</height>
        </size>
       </property>
       <property name="maximumSize">
        <size>
         <width>450</width>
         <height>16777215</height>
        </size>
       </property>
       <layout class="QVBoxLayout" name="rightPanelLayout">
        <property name="spacing">
         <number>6</number>
        </property>
        <property name="leftMargin">
         <number>6</number>
        </property>
        <property name="topMargin">
         <number>6</number>
        </property>
        <property name="rightMargin">
         <number>6</number>
        </property>
        <property name="bottomMargin">
         <number>6</number>
        </property>
        <!-- Редактор координат -->
        <item>
         <widget class="QGroupBox" name="coordinatesGroup">
          <property name="title">
           <string>Координаты</string>
          </property>
          <layout class="QGridLayout" name="coordinatesLayout">
           <item row="0" column="0">
            <widget class="QLabel" name="xLabel">
             <property name="text">
              <string>X:</string>
             </property>
            </widget>
           </item>
           <item row="0" column="1">
            <widget class="QDoubleSpinBox" name="xSpinBox">
             <property name="minimum">
              <double>-999999.000000000000000</double>
             </property>
             <property name="maximum">
              <double>999999.000000000000000</double>
             </property>
             <property name="decimals">
              <number>3</number>
             </property>
             <property name="singleStep">
              <double>1.000000000000000</double>
             </property>
            </widget>
           </item>
           <item row="0" column="2">
            <widget class="QLabel" name="aLabel">
             <property name="text">
              <string>A:</string>
             </property>
            </widget>
           </item>
           <item row="0" column="3">
            <widget class="QDoubleSpinBox" name="aSpinBox">
             <property name="minimum">
              <double>-999999.000000000000000</double>
             </property>
             <property name="maximum">
              <double>999999.000000000000000</double>
             </property>
             <property name="decimals">
              <number>3</number>
             </property>
             <property name="singleStep">
              <double>1.000000000000000</double>
             </property>
            </widget>
           </item>
           <item row="1" column="0">
            <widget class="QLabel" name="yLabel">
             <property name="text">
              <string>Y:</string>
             </property>
            </widget>
           </item>
           <item row="1" column="1">
            <widget class="QDoubleSpinBox" name="ySpinBox">
             <property name="minimum">
              <double>-999999.000000000000000</double>
             </property>
             <property name="maximum">
              <double>999999.000000000000000</double>
             </property>
             <property name="decimals">
              <number>3</number>
             </property>
             <property name="singleStep">
              <double>1.000000000000000</double>
             </property>
            </widget>
           </item>
           <item row="1" column="2">
            <widget class="QLabel" name="bLabel">
             <property name="text">
              <string>B:</string>
             </property>
            </widget>
           </item>
           <item row="1" column="3">
            <widget class="QDoubleSpinBox" name="bSpinBox">
             <property name="minimum">
              <double>-999999.000000000000000</double>
             </property>
             <property name="maximum">
              <double>999999.000000000000000</double>
             </property>
             <property name="decimals">
              <number>3</number>
             </property>
             <property name="singleStep">
              <double>1.000000000000000</double>
             </property>
            </widget>
           </item>
           <item row="2" column="0">
            <widget class="QLabel" name="zLabel">
             <property name="text">
              <string>Z:</string>
             </property>
            </widget>
           </item>
           <item row="2" column="1">
            <widget class="QDoubleSpinBox" name="zSpinBox">
             <property name="minimum">
              <double>-999999.000000000000000</double>
             </property>
             <property name="maximum">
              <double>999999.000000000000000</double>
             </property>
             <property name="decimals">
              <number>3</number>
             </property>
             <property name="singleStep">
              <double>1.000000000000000</double>
             </property>
            </widget>
           </item>
           <item row="2" column="2">
            <widget class="QLabel" name="cLabel">
             <property name="text">
              <string>C:</string>
             </property>
            </widget>
           </item>
           <item row="2" column="3">
            <widget class="QDoubleSpinBox" name="cSpinBox">
             <property name="minimum">
              <double>-999999.000000000000000</double>
             </property>
             <property name="maximum">
              <double>999999.000000000000000</double>
             </property>
             <property name="decimals">
              <number>3</number>
             </property>
             <property name="singleStep">
              <double>1.000000000000000</double>
             </property>
            </widget>
           </item>
           <item row="3" column="0" colspan="2">
            <widget class="QPushButton" name="applyCoordinatesButton">
             <property name="text">
              <string>Применить</string>
             </property>
            </widget>
           </item>
           <item row="3" column="2" colspan="2">
            <widget class="QPushButton" name="resetCoordinatesButton">
             <property name="text">
              <string>Сброс</string>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </item>
        <!-- Свойства объекта -->
        <item>
         <widget class="QGroupBox" name="propertiesGroup">
          <property name="title">
           <string>Свойства объекта</string>
          </property>
          <layout class="QVBoxLayout" name="propertiesLayout">
           <item>
            <widget class="QTableWidget" name="propertiesTable">
             <property name="columnCount">
              <number>2</number>
             </property>
             <property name="rowCount">
              <number>0</number>
             </property>
             <column>
              <property name="text">
               <string>Свойство</string>
              </property>
             </column>
             <column>
              <property name="text">
               <string>Значение</string>
              </property>
             </column>
            </widget>
           </item>
           <item>
            <layout class="QHBoxLayout" name="propertiesButtonsLayout">
             <item>
              <widget class="QPushButton" name="addPropertyButton">
               <property name="text">
                <string>Добавить</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QPushButton" name="removePropertyButton">
               <property name="text">
                <string>Удалить</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
          </layout>
         </widget>
        </item>
        <!-- Информационная панель -->
        <item>
         <widget class="QGroupBox" name="infoGroup">
          <property name="title">
           <string>Информация</string>
          </property>
          <layout class="QVBoxLayout" name="infoLayout">
           <item>
            <widget class="QTextEdit" name="infoTextEdit">
             <property name="maximumSize">
              <size>
               <width>16777215</width>
               <height>150</height>
              </size>
             </property>
             <property name="readOnly">
              <bool>true</bool>
             </property>
             <property name="plainText">
              <string>TheSolution CAD готов к работе</string>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </item>
       </layout>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
  <!-- Главное меню -->
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>1400</width>
     <height>22</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuFile">
    <property name="title">
     <string>Файл</string>
    </property>
    <addaction name="actionNew"/>
    <addaction name="actionOpen"/>
    <addaction name="actionSave"/>
    <addaction name="actionSaveAs"/>
    <addaction name="separator"/>
    <addaction name="actionExport"/>
    <addaction name="actionImport"/>
    <addaction name="separator"/>
    <addaction name="actionExit"/>
   </widget>
   <widget class="QMenu" name="menuEdit">
    <property name="title">
     <string>Правка</string>
    </property>
    <addaction name="actionUndo"/>
    <addaction name="actionRedo"/>
    <addaction name="separator"/>
    <addaction name="actionCut"/>
    <addaction name="actionCopy"/>
    <addaction name="actionPaste"/>
    <addaction name="actionDelete"/>
   </widget>
   <widget class="QMenu" name="menuView">
    <property name="title">
     <string>Вид</string>
    </property>
    <addaction name="actionFrontView"/>
    <addaction name="actionTopView"/>
    <addaction name="actionSideView"/>
    <addaction name="actionIsometricView"/>
    <addaction name="separator"/>
    <addaction name="actionZoomIn"/>
    <addaction name="actionZoomOut"/>
    <addaction name="actionZoomFit"/>
   </widget>
   <widget class="QMenu" name="menuTools">
    <property name="title">
     <string>Инструменты</string>
    </property>
    <addaction name="actionMeasure"/>
    <addaction name="actionAnalyze"/>
    <addaction name="actionSimulate"/>
   </widget>
   <widget class="QMenu" name="menuHelp">
    <property name="title">
     <string>Справка</string>
    </property>
    <addaction name="actionAbout"/>
    <addaction name="actionDocumentation"/>
   </widget>
   <addaction name="menuFile"/>
   <addaction name="menuEdit"/>
   <addaction name="menuView"/>
   <addaction name="menuTools"/>
   <addaction name="menuHelp"/>
  </widget>
  <!-- Главная панель инструментов -->
  <widget class="QToolBar" name="mainToolBar">
   <property name="windowTitle">
    <string>Главная панель инструментов</string>
   </property>
   <property name="toolButtonStyle">
    <enum>Qt::ToolButtonIconOnly</enum>
   </property>
   <addaction name="actionNew"/>
   <addaction name="actionOpen"/>
   <addaction name="actionSave"/>
   <addaction name="separator"/>
   <addaction name="actionUndo"/>
   <addaction name="actionRedo"/>
   <addaction name="separator"/>
   <addaction name="actionZoomIn"/>
   <addaction name="actionZoomOut"/>
   <addaction name="actionZoomFit"/>
  </widget>
  <!-- Статусная строка -->
  <widget class="QStatusBar" name="statusbar"/>
  <!-- Действия -->
  <action name="actionNew">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/new.png</normaloff>:/icons/new.png</iconset>
   </property>
   <property name="text">
    <string>Новый</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+N</string>
   </property>
  </action>
  <action name="actionOpen">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/open.png</normaloff>:/icons/open.png</iconset>
   </property>
   <property name="text">
    <string>Открыть</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+O</string>
   </property>
  </action>
  <action name="actionSave">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/save.png</normaloff>:/icons/save.png</iconset>
   </property>
   <property name="text">
    <string>Сохранить</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+S</string>
   </property>
  </action>
  <action name="actionSaveAs">
   <property name="text">
    <string>Сохранить как...</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+Shift+S</string>
   </property>
  </action>
  <action name="actionExport">
   <property name="text">
    <string>Экспорт</string>
   </property>
  </action>
  <action name="actionImport">
   <property name="text">
    <string>Импорт</string>
   </property>
  </action>
  <action name="actionExit">
   <property name="text">
    <string>Выход</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+Q</string>
   </property>
  </action>
  <action name="actionUndo">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/undo.png</normaloff>:/icons/undo.png</iconset>
   </property>
   <property name="text">
    <string>Отменить</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+Z</string>
   </property>
  </action>
  <action name="actionRedo">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/redo.png</normaloff>:/icons/redo.png</iconset>
   </property>
   <property name="text">
    <string>Повторить</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+Y</string>
   </property>
  </action>
  <action name="actionCut">
   <property name="text">
    <string>Вырезать</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+X</string>
   </property>
  </action>
  <action name="actionCopy">
   <property name="text">
    <string>Копировать</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+C</string>
   </property>
  </action>
  <action name="actionPaste">
   <property name="text">
    <string>Вставить</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+V</string>
   </property>
  </action>
  <action name="actionDelete">
   <property name="text">
    <string>Удалить</string>
   </property>
   <property name="shortcut">
    <string>Del</string>
   </property>
  </action>
  <action name="actionZoomIn">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/zoom_in.png</normaloff>:/icons/zoom_in.png</iconset>
   </property>
   <property name="text">
    <string>Увеличить</string>
   </property>
   <property name="shortcut">
    <string>Ctrl++</string>
   </property>
  </action>
  <action name="actionZoomOut">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/zoom_out.png</normaloff>:/icons/zoom_out.png</iconset>
   </property>
   <property name="text">
    <string>Уменьшить</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+-</string>
   </property>
  </action>
  <action name="actionZoomFit">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/zoom_fit.png</normaloff>:/icons/zoom_fit.png</iconset>
   </property>
   <property name="text">
    <string>По размеру</string>
   </property>
   <property name="shortcut">
    <string>Ctrl+0</string>
   </property>
  </action>
  <action name="actionRotate">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/rotate.png</normaloff>:/icons/rotate.png</iconset>
   </property>
   <property name="text">
    <string>Вращение</string>
   </property>
  </action>
  <action name="actionPan">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/pan.png</normaloff>:/icons/pan.png</iconset>
   </property>
   <property name="text">
    <string>Перемещение</string>
   </property>
  </action>
  <action name="actionSelect">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/select.png</normaloff>:/icons/select.png</iconset>
   </property>
   <property name="text">
    <string>Выбор</string>
   </property>
  </action>
  <action name="actionFrontView">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/front_view.png</normaloff>:/icons/front_view.png</iconset>
   </property>
   <property name="text">
    <string>Вид спереди</string>
   </property>
   <property name="shortcut">
    <string>F1</string>
   </property>
  </action>
  <action name="actionTopView">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/top_view.png</normaloff>:/icons/top_view.png</iconset>
   </property>
   <property name="text">
    <string>Вид сверху</string>
   </property>
   <property name="shortcut">
    <string>F2</string>
   </property>
  </action>
  <action name="actionSideView">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/side_view.png</normaloff>:/icons/side_view.png</iconset>
   </property>
   <property name="text">
    <string>Вид сбоку</string>
   </property>
   <property name="shortcut">
    <string>F3</string>
   </property>
  </action>
  <action name="actionIsometricView">
   <property name="icon">
    <iconset>
     <normaloff>:/icons/isometric_view.png</normaloff>:/icons/isometric_view.png</iconset>
   </property>
   <property name="text">
    <string>Изометрический вид</string>
   </property>
   <property name="shortcut">
    <string>F4</string>
   </property>
  </action>
  <action name="actionMeasure">
   <property name="text">
    <string>Измерения</string>
   </property>
  </action>
  <action name="actionAnalyze">
   <property name="text">
    <string>Анализ</string>
   </property>
  </action>
  <action name="actionSimulate">
   <property name="text">
    <string>Симуляция</string>
   </property>
  </action>
  <action name="actionAbout">
   <property name="text">
    <string>О программе</string>
   </property>
  </action>
  <action name="actionDocumentation">
   <property name="text">
    <string>Документация</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>
