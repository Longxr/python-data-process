#ifndef COURSETABWIDGETCONTROLLER_H
#define COURSETABWIDGETCONTROLLER_H

#include <JYUIKit/JYUIKit.h>

class CourseTabWidgetCallback
{
public:
//    virtual void OnCallXXX() = 0;
};

class CourseTabWidget : public JYWidget
{
    Q_OBJECT
public:
    explicit CourseTabWidget(QWidget *parent = nullptr);
    ~CourseTabWidget();

    virtual void SetCallback(CourseTabWidgetCallback * pCallback);

private:
    QHBoxLayout* MainLayout();

    CourseTabWidgetCallback*     m_pCallback;
    QHBoxLayout*            m_pMainLayout;
};

class CourseTabWidgetController  : public JYWidgetController
                              , public CourseTabWidgetCallback
{
    Q_OBJECT
public:
    CourseTabWidgetController();
    ~CourseTabWidgetController();

    //CourseTabWidgetCallback
//    virtual void OnCallXXX();

    //JYWidgetController
    virtual QWidget *Widget();

    CourseTabWidget* GetCourseTabWidget();

private:
    CourseTabWidget*     m_pCourseTabWidget;
};

#endif // COURSETABWIDGETCONTROLLER_H
