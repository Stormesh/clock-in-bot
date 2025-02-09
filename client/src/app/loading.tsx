import React from "react";
import GearSpin from "./components/GearSpin";

const Loading = () => {
  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <GearSpin />
      <h2 className="text-center font-light text-2xl text-white font-sans">
        Loading...
      </h2>
    </div>
  );
};

export default Loading;
