#include "sensor_view_widget.h"
#include "viewpic.h"
#include <QLabel>
#include <QDir>
#include <QDebug>

SensorViewWidget::SensorViewWidget(const QString &name, QWidget *parent)
    : QTabWidget(parent), m_name(name)
{
    m_str_label["Euler"] = new ViewPic("E");
    m_str_label["Rotate"] = new ViewPic("R");
    m_str_label["Mag"] = new ViewPic("M");
    m_str_label["TotalGyro"] = new ViewPic("TG");
    m_str_label["Gyro"] = new ViewPic("G");
    m_str_label["TotalAcce"] = new ViewPic("TA");
    m_str_label["Acce"] = new ViewPic("A");

    for(auto ite = m_str_label.begin(); ite != m_str_label.end(); ++ite) {
        addTab(ite.value(), ite.key());
    }
    setCurrentIndex(0);
    resize(sizeHint());
}

SensorViewWidget::~SensorViewWidget()
{
    for(auto ite = m_str_label.begin(); ite != m_str_label.end(); ++ite) {
        delete ite.value();
    }
}

QString SensorViewWidget::name() const
{
    return m_name;
}

void SensorViewWidget::setName(const QString &name)
{
    m_name = name;
}

void SensorViewWidget::load_xml_file(const QDir& pic_dir, const QString& file_name)
{
    for(QString& str : pic_dir.entryList()) {
        if(!str.contains(file_name)) continue;

        for(auto ite = m_str_label.begin(); ite != m_str_label.end(); ++ite) {
            if(str.contains("_" + ite.value()->index_name())) {
                m_str_label[ite.key()]->setPixmap(QPixmap(pic_dir.filePath(str)));
                break;
            }
        }
    }
}

