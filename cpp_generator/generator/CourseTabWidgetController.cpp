#include "CourseTabWidgetController.h"

/*********************************************************************************
 * CourseTabWidget
 *
 *********************************************************************************/

CourseTabWidget::CourseTabWidget(QWidget *parent) : JYWidget(parent)
{
    m_pMainLayout = nullptr;

    this->setLayout(MainLayout());
}

CourseTabWidget::~CourseTabWidget()
{

}

void CourseTabWidget::SetCallback(CourseTabWidgetCallback *pCallback)
{
    m_pCallback = pCallback;
}

QHBoxLayout* MainLayout()
{
    if (nullptr == m_pMainLayout) {
        m_pMainLayout = new QHBoxLayout(this);
        m_pMainLayout->setContentsMargins(0, 0, 0, 0);
        m_pMainLayout->setSpacing(0);
    }

    return m_pMainLayout;
}

/*********************************************************************************
 * CourseTabWidgetController
 *
 *********************************************************************************/

CourseTabWidgetController::CourseTabWidgetController()
{
    m_pCourseTabWidget = nullptr;
}

CourseTabWidgetController::~CourseTabWidgetController()
{
    JY_RELEASE_CLASS(m_pCourseTabWidget)
}

//void HomeWidgetController::OnCallXXX()
//{

//}

QWidget *CourseTabWidgetController::Widget()
{
    if(0x0 == m_pCourseTabWidget) {
        m_pCourseTabWidget = new CourseTabWidget();
        m_pCourseTabWidget->SetCallback(this);

        m_pCourseTabWidget->setMinimumSize(892, 451);
    }

    return m_pCourseTabWidget;
}

CourseTabWidget* GetCourseTabWidget()
{
    return qobject_cast<CourseTabWidget *>(Widget());
}
