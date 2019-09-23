QHBoxLayout *AnswerStatisticsWidget::GetMainLayout()
{
    if (nullptr == m_pMainLayout) {
        m_pMainLayout = new QHBoxLayout();
        m_pMainLayout->setContentsMargins(0, 0, 0, 0);
        m_pMainLayout->setSpacing(0);
    }

    return m_pMainLayout;
}

JYWidget *AnswerStatisticsWidget::GetTopListWidget()
{
    if (nullptr == m_pTopListWidget) {
        m_pTopListWidget = new JYWidget(this);
    }

    return m_pTopListWidget;
}

JYWidget *AnswerStatisticsWidget::GetHistogramWidget()
{
    if (nullptr == m_pHistogramWidget) {
        m_pHistogramWidget = new JYWidget(this);
    }

    return m_pHistogramWidget;
}

JYWidget *AnswerStatisticsWidget::GetBottomWidget()
{
    if (nullptr == m_pBottomWidget) {
        m_pBottomWidget = new JYWidget(this);
    }

    return m_pBottomWidget;
}

QListView *AnswerStatisticsWidget::GetStudentListView()
{
    if (nullptr == m_pStudentListView) {
        m_pStudentListView = new QListView(this);
    }

    return m_pStudentListView;
}

QLabel *AnswerStatisticsWidget::GetCountLabel()
{
    if (nullptr == m_pCountLabel) {
        m_pCountLabel = new QLabel(this);
    }

    return m_pCountLabel;
}

QPushButton *AnswerStatisticsWidget::GetScreenBtn()
{
    if (nullptr == m_pScreenBtn) {
        m_pScreenBtn = new QPushButton(this);
    }

    return m_pScreenBtn;
}

QPushButton *AnswerStatisticsWidget::GetStopBtn()
{
    if (nullptr == m_pStopBtn) {
        m_pStopBtn = new QPushButton(this);
    }

    return m_pStopBtn;
}

QPushButton *AnswerStatisticsWidget::GetCancleBtn()
{
    if (nullptr == m_pCancleBtn) {
        m_pCancleBtn = new QPushButton(this);
    }

    return m_pCancleBtn;
}


m_pMainLayout = nullptr;
m_pTopListWidget = nullptr;
m_pHistogramWidget = nullptr;
m_pBottomWidget = nullptr;
m_pStudentListView = nullptr;
m_pCountLabel = nullptr;
m_pScreenBtn = nullptr;
m_pStopBtn = nullptr;
m_pCancleBtn = nullptr;
