#include "LocalCourseWidgetController.h"

/*********************************************************************************
 * LocalCourseWidget
 *
 *********************************************************************************/

LocalCourseWidget::LocalCourseWidget(QWidget *parent) : JYWidget(parent)
{
    m_pMainLayout = nullptr;

    this->setLayout(MainLayout());
}

LocalCourseWidget::~LocalCourseWidget()
{

}

void LocalCourseWidget::SetCallback(LocalCourseWidgetCallback *pCallback)
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
 * LocalCourseWidgetController
 *
 *********************************************************************************/

LocalCourseWidgetController::LocalCourseWidgetController()
{
    m_pLocalCourseWidget = nullptr;
}

LocalCourseWidgetController::~LocalCourseWidgetController()
{
    JY_RELEASE_CLASS(m_pLocalCourseWidget)
}

//void HomeWidgetController::OnCallXXX()
//{

//}

QWidget *LocalCourseWidgetController::Widget()
{
    if(0x0 == m_pLocalCourseWidget) {
        m_pLocalCourseWidget = new LocalCourseWidget();
        m_pLocalCourseWidget->SetCallback(this);

        m_pLocalCourseWidget->setMinimumSize(892, 451);
    }

    return m_pLocalCourseWidget;
}

LocalCourseWidget* GetLocalCourseWidget()
{
    return qobject_cast<LocalCourseWidget *>(Widget());
}
