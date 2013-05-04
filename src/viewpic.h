#ifndef VIEWPIC_H
#define VIEWPIC_H

#include <QLabel>

class ViewPic : public QLabel
{
    Q_OBJECT
public:
    ViewPic(const QString& index_name, QWidget *parent = 0);
    
    QString index_name() const;
    void setIndex_name(const QString &index_name);

signals:
    
public slots:
    
private:
    QString m_index_name;
};

#endif // VIEWPIC_H
