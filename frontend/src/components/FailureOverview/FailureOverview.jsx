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

const options = {
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
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, { retryOnError: true });
  const [serverData, setServerData] = useState([
    {
      labels: [new Date().toLocaleTimeString()],
      datasets: [
        {
          label: "Success (%)",
          data: [0],
          backgroundColor: "rgba(0, 255, 0, 1)",
        },
        {
          label: "Fail (%)",
          data: [0],
          backgroundColor: "rgba(255, 0, 0, 1)",
        },
      ],
    },
    {
      labels: [new Date().toLocaleTimeString()],
      datasets: [
        {
          label: "Difference (%)",
          data: [0],
          backgroundColor: "rgba(0, 0, 0, 1)",
        },
      ],
    },
  ]);

  useEffect(() => {
    if (lastMessage !== null) {
      // console.log(lastMessage.data)
      let res = JSON.parse(lastMessage.data);
      // console.log(res)

      if (res["regular"] != null) {
        // set regular state
      } else if (res["ov"] != null) {
        let newServerData = [
          {
            labels: [...serverData[0].labels, new Date().toLocaleTimeString()],
            datasets: [
              {
                label: "Success (%)",
                data: [...serverData[0].datasets[0].data, res.ov.dnn.success],
                backgroundColor: serverData[0].datasets[0].backgroundColor,
              },
              {
                label: "Fail (%)",
                data: [...serverData[0].datasets[1].data, res.ov.dnn.fail],
                backgroundColor: serverData[0].datasets[1].backgroundColor,
              },
            ],
          },
          {
            labels: [...serverData[1].labels, new Date().toLocaleTimeString()],
            datasets: [
              {
                label: "Difference (%)",
                data: [...serverData[1].datasets[0].data, res.ov.cv.difference],
                backgroundColor: serverData[1].datasets[0].backgroundColor,
              },
            ],
          },
        ];

        if (newServerData[0].datasets[0].data.length > 20) {
          newServerData[0].datasets[0].data.shift()
          newServerData[0].datasets[1].data.shift()
          newServerData[0].labels.shift()
          newServerData[1].datasets[0].data.shift()
          newServerData[1].labels.shift()
        }

        setServerData([...newServerData]);
      }
    }
  }, [lastMessage]);

  return (
    <ModuleContainer>
      <StatusCard>Failure Mode Overview</StatusCard>
      <StatusCard>
        Deep Neural Network
        <Line options={options} data={serverData[0]} />
      </StatusCard>
      <StatusCard>
        Computer Vision
        <Line options={options} data={serverData[1]} />
      </StatusCard>
    </ModuleContainer>
  );
}
