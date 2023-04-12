import ModuleContainer from "../ModuleContainer"
import { StatusCard } from "../StatusCard"

export default function FailureOverview() {
    return (
        <ModuleContainer>
            <StatusCard>
                Failure Mode Overview
            </StatusCard>
            <StatusCard>
                Deep Neural Network
                <img style={{ width: "100%" }} src="https://ppcexpo.com/blog/wp-content/uploads/2022/07/time-series-graph-examples.jpg" alt="" />
                Status: Success (95% Confidence)
            </StatusCard>
            <StatusCard>
                Computer Vision
                <img style={{ width: "100%" }} src="https://ppcexpo.com/blog/wp-content/uploads/2022/07/time-series-graph-examples.jpg" alt="" />
                Status: Success Difference 5% (&lt;30%)
            </StatusCard>
            <StatusCard>
                <StatusCard>
                    History (Last 50 Results)
                </StatusCard>
                DNN: 50 Success, 0 Fail <br />
                CV: 50 Success, 0 Fail
            </StatusCard>
        </ModuleContainer>
    )
}