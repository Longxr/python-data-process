QHBoxLayout *CourseItemWidget::GetMainLayout()
{
    if (nullptr == m_pMainLayout) {
        m_pMainLayout = new QHBoxLayout(this);
    }

    return m_pMainLayout;
}
QComboBox *CourseItemWidget::GetQComboBox()
{
    if (nullptr == m_pQComboBox) {
        m_pQComboBox = new QComboBox(this);
    }

    return m_pQComboBox;
}
QPushButton *CourseItemWidget::GetEnterBtn()
{
    if (nullptr == m_pEnterBtn) {
        m_pEnterBtn = new QPushButton(this);
    }

    return m_pEnterBtn;
}

m_pMainLayout = nullptr;
m_pQComboBox = nullptr;
m_pEnterBtn = nullptr;
