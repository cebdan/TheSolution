<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1465</width>
    <height>800</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>TheSolution CAD - Let's Do Solution</string>
  </property>
  <property name="styleSheet">
   <string notr="true">/* Основные стили */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #2c3e50, stop:1 #34495e);
    color: white;
}

/* Заголовок */
QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3498db, stop:1 #2980b9);
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}

/* Кнопки решений */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3498db, stop:1 #2980b9);
    border: 2px solid #2980b9;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    padding: 12px;
    font-size: 14px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5dade2, stop:1 #3498db);
    border: 2px solid #5dade2;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2980b9, stop:1 #1f618d);
}

/* Кнопки приоритетных решений */
QPushButton#priorityButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e74c3c, stop:1 #c0392b);
    border: 2px solid #c0392b;
}

QPushButton#priorityButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ec7063, stop:1 #e74c3c);
    border: 2px solid #ec7063;
}

/* Панели */
QFrame {
    background: rgba(52, 73, 94, 0.8);
    border: 2px solid #34495e;
    border-radius: 10px;
}

/* Дерево решений */
QTreeWidget {
    background: rgba(44, 62, 80, 0.9);
    border: 2px solid #34495e;
    border-radius: 8px;
    color: white;
    font-size: 13px;
}

QTreeWidget::item {
    padding: 8px;
    border-bottom: 1px solid #34495e;
}

QTreeWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3498db, stop:1 #2980b9);
}

QTreeWidget::item:hover {
    background: rgba(52, 152, 219, 0.3);
}

/* Текстовые поля */
QTextEdit {
    background: rgba(44, 62, 80, 0.9);
    border: 2px solid #34495e;
    border-radius: 8px;
    color: white;
    font-family: &quot;Consolas&quot;, monospace;
    font-size: 12px;
}

/* Метки */
QLabel {
    color: white;
    font-weight: bold;
}

QLabel#titleLabel {
    font-size: 24px;
    color: #3498db;
    font-weight: bold;
}

QLabel#subtitleLabel {
    font-size: 16px;
    color: #bdc3c7;
}

/* Статус бар */
QStatusBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #34495e, stop:1 #2c3e50);
    color: white;
    border-top: 2px solid #3498db;
}

/* Прогресс бар */
QProgressBar {
    border: 2px solid #34495e;
    border-radius: 5px;
    text-align: center;
    color: white;
    font-weight: bold;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #27ae60, stop:1 #229954);
    border-radius: 3px;
}</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QHBoxLayout" name="horizontalLayout">
    <item>
     <widget class="QFrame" name="leftPanel">
      <property name="minimumSize">
       <size>
        <width>300</width>
        <height>0</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>350</width>
        <height>16777215</height>
       </size>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_2">
       <item>
        <widget class="QLabel" name="titleLabel">
         <property name="text">
          <string>🎯 Let's Do Solution</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QLabel" name="subtitleLabel">
         <property name="text">
          <string>TheSolution CAD Platform</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QTreeWidget" name="solutionsTree">
         <property name="headerLabel" stdset="0">
          <string>Решения</string>
         </property>
         <column>
          <property name="text">
           <string>Статус</string>
          </property>
         </column>
         <column>
          <property name="text">
           <string>Тип</string>
          </property>
         </column>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="refreshButton">
         <property name="text">
          <string>🔄 Обновить</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QFrame" name="centerPanel">
      <layout class="QVBoxLayout" name="verticalLayout">
       <item>
        <widget class="QLabel" name="solutionTitleLabel">
         <property name="text">
          <string>Выберите решение для работы</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QScrollArea" name="scrollArea">
         <property name="widgetResizable">
          <bool>true</bool>
         </property>
         <widget class="QWidget" name="scrollAreaWidgetContents">
          <property name="geometry">
           <rect>
            <x>0</x>
            <y>0</y>
            <width>709</width>
            <height>692</height>
           </rect>
          </property>
          <layout class="QGridLayout" name="gridLayout">
           <item row="0" column="0">
            <widget class="QFrame" name="frame_3d">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_3">
              <item>
               <widget class="QLabel" name="label_3d">
                <property name="text">
                 <string>🎯 3D-Solution (ПРИОРИТЕТ)</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launch3DButton">
                <property name="text">
                 <string>🚀 3D-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="create3DObjectsButton">
                <property name="text">
                 <string>🔸 Создать 3D объекты</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="geometryButton">
                <property name="text">
                 <string>📐 Работа с геометрией</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item row="0" column="1">
            <widget class="QFrame" name="frame_2d">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_4">
              <item>
               <widget class="QLabel" name="label_2d">
                <property name="text">
                 <string>📐 2D-Solution</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launch2DButton">
                <property name="text">
                 <string>🚀 Запустить 2D-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="createDrawingsButton">
                <property name="text">
                 <string>📋 Создать чертежи</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item row="1" column="0">
            <widget class="QFrame" name="frame_assembly">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_5">
              <item>
               <widget class="QLabel" name="label_assembly">
                <property name="text">
                 <string>🔧 Assembly-Solution</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launchAssemblyButton">
                <property name="text">
                 <string>🚀 Запустить Assembly-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="createAssembliesButton">
                <property name="text">
                 <string>🔧 Создать сборки</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item row="1" column="1">
            <widget class="QFrame" name="frame_analysis">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_6">
              <item>
               <widget class="QLabel" name="label_analysis">
                <property name="text">
                 <string>📊 Analysis-Solution</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launchAnalysisButton">
                <property name="text">
                 <string>🚀 Запустить Analysis-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="analysisButton">
                <property name="text">
                 <string>📊 Анализ и расчеты</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item row="2" column="0">
            <widget class="QFrame" name="frame_simulation">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_7">
              <item>
               <widget class="QLabel" name="label_simulation">
                <property name="text">
                 <string>🔄 Simulation-Solution</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launchSimulationButton">
                <property name="text">
                 <string>🚀 Запустить Simulation-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="simulationButton">
                <property name="text">
                 <string>🔄 Симуляция и тестирование</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item row="2" column="1">
            <widget class="QFrame" name="frame_manufacturing">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_8">
              <item>
               <widget class="QLabel" name="label_manufacturing">
                <property name="text">
                 <string>🏭 Manufacturing-Solution</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launchManufacturingButton">
                <property name="text">
                 <string>🚀 Запустить Manufacturing-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="manufacturingButton">
                <property name="text">
                 <string>🏭 Производство и CAM</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item row="3" column="0">
            <widget class="QFrame" name="frame_documentation">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_9">
              <item>
               <widget class="QLabel" name="label_documentation">
                <property name="text">
                 <string>📄 Documentation-Solution</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launchDocumentationButton">
                <property name="text">
                 <string>🚀 Запустить Documentation-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="documentationButton">
                <property name="text">
                 <string>📄 Документооборот</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item row="3" column="1">
            <widget class="QFrame" name="frame_collaboration">
             <property name="frameShape">
              <enum>QFrame::StyledPanel</enum>
             </property>
             <property name="frameShadow">
              <enum>QFrame::Raised</enum>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_10">
              <item>
               <widget class="QLabel" name="label_collaboration">
                <property name="text">
                 <string>👥 Collaboration-Solution</string>
                </property>
                <property name="alignment">
                 <set>Qt::AlignCenter</set>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="launchCollaborationButton">
                <property name="text">
                 <string>🚀 Запустить Collaboration-Solution</string>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QPushButton" name="collaborationButton">
                <property name="text">
                 <string>👥 Совместная работа</string>
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
    </item>
    <item>
     <widget class="QFrame" name="rightPanel">
      <property name="minimumSize">
       <size>
        <width>300</width>
        <height>0</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>350</width>
        <height>16777215</height>
       </size>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_11">
       <item>
        <widget class="QLabel" name="toolsLabel">
         <property name="text">
          <string>🛠️ Инструменты</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="rootLauncherButton">
         <property name="text">
          <string>🏗️ Root Solution Launcher</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="demoButton">
         <property name="text">
          <string>🎬 Демонстрация возможностей</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="testButton">
         <property name="text">
          <string>🧪 Тестирование системы</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="infoButton">
         <property name="text">
          <string>📋 Информация о решениях</string>
         </property>
        </widget>
       </item>
       <item>
        <spacer name="verticalSpacer">
         <property name="orientation">
          <enum>Qt::Vertical</enum>
         </property>
         <property name="sizeHint" stdset="0">
          <size>
           <width>20</width>
           <height>40</height>
          </size>
         </property>
        </spacer>
       </item>
       <item>
        <widget class="QLabel" name="statusLabel">
         <property name="text">
          <string>Статус: Готов к работе</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QProgressBar" name="progressBar">
         <property name="value">
          <number>100</number>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QTextEdit" name="logTextEdit">
         <property name="maximumSize">
          <size>
           <width>16777215</width>
           <height>150</height>
          </size>
         </property>
         <property name="placeholderText">
          <string>Лог событий...</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>1465</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menuFile">
    <property name="title">
     <string>Файл</string>
    </property>
    <addaction name="actionExit"/>
   </widget>
   <widget class="QMenu" name="menuHelp">
    <property name="title">
     <string>Помощь</string>
    </property>
    <addaction name="actionAbout"/>
   </widget>
   <addaction name="menuFile"/>
   <addaction name="menuHelp"/>
  </widget>
  <action name="actionExit">
   <property name="text">
    <string>Выход</string>
   </property>
  </action>
  <action name="actionAbout">
   <property name="text">
    <string>О программе</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>
