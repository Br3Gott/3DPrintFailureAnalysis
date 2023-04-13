import ModuleContainer from "../ModuleContainer";
import useWebSocket from "react-use-websocket";
import { StatusCard } from "../StatusCard";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import faker from "faker";
import { useState, useEffect } from "react";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const labels = ["January", "February", "March", "April", "May", "June", "July"];

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top",
    },
    title: {
      display: true,
      text: "History",
    },
  },
};

export default function FailureOverview({ socketUrl }) {
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [serverData, setServerData] = useState(
    {
      labels: [0],
      dnn: {
        success: 0,
        fail: 0
      },
      cv: {
        difference: 0
      }
    }
  );

  var data = {
    labels: [...serverData.labels],
    datasets: [
      {
        label: "Success",
        data: [...[serverData.dnn.success]],
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
      {
        label: "Fail",
        data: [...[serverData.dnn.fail]],
        backgroundColor: "rgba(53, 162, 235, 0.5)",
      },
    ],
  };
  console.log(data)

  useEffect(() => {
    if (lastMessage !== null) {
      // console.log(lastMessage.data)
      let res = JSON.parse(lastMessage.data);
      // console.log(res)

      if (res["regular"] != null) {
        // set regular state
      } else if (res["ov"] != null) {
        // setStats(res["ps"])
        console.log("hej ov");
        setServerData(res["ov"]);
        console.log(res["ov"]);
      }
    }
  }, [lastMessage]);

  return (
    <ModuleContainer>
      <StatusCard>Failure Mode Overview</StatusCard>
      <StatusCard>
        Deep Neural Network
        <Line options={options} data={data} />
        Status: Success (95% Confidence)
      </StatusCard>
      <StatusCard>
        Computer Vision
        <Line options={options} data={data} />
        Status: Success Difference 5% (&lt;30%)
      </StatusCard>
      {/* <StatusCard>
        <StatusCard>History (Last 50 Results)</StatusCard>
        DNN: 50 Success, 0 Fail <br />
        CV: 50 Success, 0 Fail
      </StatusCard> */}
    </ModuleContainer>
  );
}
