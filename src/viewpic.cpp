#include "viewpic.h"

ViewPic::ViewPic(const QString &index_name, QWidget *parent) :
    QLabel(parent), m_index_name(index_name)
{
    setScaledContents(true);
}

QString ViewPic::index_name() const
{
    return m_index_name;
}

void ViewPic::setIndex_name(const QString &index_name)
{
    m_index_name = index_name;
}
