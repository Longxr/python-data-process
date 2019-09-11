#ifndef LOCALCOURSEWIDGETCONTROLLER_H
#define LOCALCOURSEWIDGETCONTROLLER_H

#include <JYUIKit/JYUIKit.h>

class LocalCourseWidgetCallback
{
public:
//    virtual void OnCallXXX() = 0;
};

class LocalCourseWidget : public JYWidget
{
    Q_OBJECT
public:
    explicit LocalCourseWidget(QWidget *parent = nullptr);
    ~LocalCourseWidget();

    virtual void SetCallback(LocalCourseWidgetCallback * pCallback);

private:
    QHBoxLayout* MainLayout();

    LocalCourseWidgetCallback*     m_pCallback;
    QHBoxLayout*            m_pMainLayout;
};

class LocalCourseWidgetController  : public JYWidgetController
                              , public LocalCourseWidgetCallback
{
    Q_OBJECT
public:
    LocalCourseWidgetController();
    ~LocalCourseWidgetController();

    //LocalCourseWidgetCallback
//    virtual void OnCallXXX();

    //JYWidgetController
    virtual QWidget *Widget();

    LocalCourseWidget* GetLocalCourseWidget();

private:
    LocalCourseWidget*     m_pLocalCourseWidget;
};

#endif // LOCALCOURSEWIDGETCONTROLLER_H
