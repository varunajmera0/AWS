import React from "react";
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
// import faker from 'faker';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top",
    },
    title: {
      display: true,
      text: "Stock",
    },
  },
};

// const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

export function GraphLine({ data }) {
  console.log("Graph line", data);
  const labels = data?.map((d) => d.datetime);
  const data_ = {
    labels,
    datasets: [
      {
        label: `Close Drop for ${data?.[0]?.symbol || ""}`,
        data: data?.map((d) => d.closedrop),
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: [
          "rgba(75,192,192,1)",
          "#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0",
        ],
        borderWidth: 2,
      },
    ],
  };
  return <Line options={options} data={data_} />;
}
