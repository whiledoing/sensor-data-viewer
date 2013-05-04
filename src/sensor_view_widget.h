#ifndef SENSOR_VIEW_WIDGET_H
#define SENSOR_VIEW_WIDGET_H

#include <QTabWidget>
#include <QDir>
#include <QMap>
#include <QLabel>
class ViewPic;

class SensorViewWidget : public QTabWidget
{
    Q_OBJECT
public:
    SensorViewWidget(const QString& name, QWidget *parent = 0);
    ~SensorViewWidget();
    
    void load_xml_file(const QDir &pic_dir, const QString &file_name);
    QString name() const;
    void setName(const QString &name);

signals:
    
public slots:

private:
    QString m_name;
    QMap<QString, ViewPic*> m_str_label;
};

#endif // SENSOR_VIEW_WIDGET_H
