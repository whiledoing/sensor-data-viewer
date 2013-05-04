#include "sensor_view.h"
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QFileSystemModel>
#include <QtWidgets/QTreeView>
#include <QtCore/QStringList>
#include <QMessageBox>
#include <QProcess>
#include <QtDebug>
#include <QtWidgets/QLabel>
#include <QSettings>
#include "sensor_view_widget.h"

Widget::Widget(QWidget *parent) :
    QWidget(parent)
{
    setupUi(this);

    m_model = new QFileSystemModel(this);
    QStringList list;
    list << "*.xml";
    m_model->setNameFilters(list);

    QString list_dir = "F:/sensor/python_sensor/session_files";
    m_model->setRootPath(list_dir);

    m_tree_view->setModel(m_model);
    m_tree_view->setWindowTitle(QObject::tr("Xml Viewer"));
    m_tree_view->setRootIndex(m_model->index(list_dir));
    m_tree_view->hideColumn(1);
    m_tree_view->hideColumn(2);
    m_tree_view->hideColumn(3);
}

Widget::~Widget()
{
}

bool exist_jpg_file(QString file_path)
{
    auto file_name = QFileInfo(file_path).baseName();

    auto par_dir = QFileInfo(file_path).dir();

    if(par_dir.exists("pic")) {
        QStringList filters;
        filters << "*.jpg";

        QDir pic_dir = par_dir.absolutePath() + QDir::separator() + "pic";
        auto sensor_list= pic_dir.entryList();
        if(sensor_list.size() == 2) return false;

        // check into the sensor node list
        pic_dir.cd(sensor_list.at(2));
        qDebug() << "pic find dir : " << pic_dir;
        pic_dir.setNameFilters(filters);

        foreach(const QString &str, pic_dir.entryList()) {
            qDebug() << str;
            if(str.contains(file_name)) {
                return true;
            }
        }
    }
    return false;
}

inline QDir get_script_dir()
{
    QDir cur_dir(qApp->applicationDirPath());
    cur_dir.cdUp();
    cur_dir.cdUp();
    return cur_dir;
}

bool create_pic(const QString& file_path)
{
    QProcess process;
    QString program = "python.exe";

    QString py_path = get_script_dir().absoluteFilePath("draw_graph/draw.py");
    qDebug() << "python path : " << py_path;

    if(!QFileInfo(py_path).exists()) {
        QMessageBox::warning(NULL, QObject::tr("warning"), QObject::tr("not exist python file"));
        return false;
    }

    QStringList arguments;
    arguments << py_path << file_path;

    QApplication::setOverrideCursor(QCursor(Qt::WaitCursor));
    process.start(program, arguments);

    bool finished = process.waitForFinished();
    QApplication::restoreOverrideCursor();

    return finished;
}

SensorViewWidget* get_widget(QTabWidget* tab_widget, const QString& name)
{
    for(int i = 0; i < tab_widget->count(); ++i) {
        SensorViewWidget* widget = (SensorViewWidget*)(tab_widget->widget(i));
        if(widget->name() == name)  return widget;
    }
    return static_cast<SensorViewWidget*>(tab_widget->widget(tab_widget->addTab(new SensorViewWidget(name), name)));
}

void Widget::on_m_tree_view_doubleClicked(const QModelIndex &index)
{\
    auto file_path = QFileInfo(m_model->filePath(index)).absoluteFilePath();
    auto file_name = QFileInfo(file_path).baseName();

    // generate pic
    if(!exist_jpg_file(file_path)) {
        if(!create_pic(file_path))
            return;
    }

    auto pic_dir = QFileInfo(file_path).dir();
    if(!pic_dir.cd("pic"))  return;

    // find node count in the generated pic directory
    auto sensor_list = pic_dir.entryList(QDir::Dirs);
    for(int i = 0; i < sensor_list.size(); ++i) {
        if(sensor_list.at(i)[0] == '.') continue;
        auto widget = get_widget(m_img_tab, sensor_list.at(i));
        widget->load_xml_file(pic_dir.absoluteFilePath(sensor_list.at(i)), file_name);
    }

    // if all success here, update step count according to step_count.txt
    m_step_count_label->setText("");
    bool bOk = false;
    int data_count = file_name.toInt(&bOk);
    if(!bOk) return;

    QString step_count_file_name = QFileInfo(file_path).dir().absoluteFilePath("step_count.txt");
    QFile file(step_count_file_name);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return;

    QTextStream in(&file);
    QString line;
    for(int i = 0; i < data_count - 1; ++i) {
        in.readLine();
    }

    if(in.atEnd()) return;
    QString m_cur_line = in.readLine();

    auto number_list = m_cur_line.split(' ');
    QString result;
    int total_count = 0;
    foreach(QString str, number_list) {
        result += "Step : " + str + '\t';
        total_count += str.toInt();
    }
    result += "<b>Total : " + QString::number(total_count) + "</b>";
    m_step_count_label->setText(result);
}

