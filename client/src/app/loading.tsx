import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGear } from "@fortawesome/free-solid-svg-icons";

const Loading = () => {
  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <FontAwesomeIcon
        icon={faGear}
        width={60}
        height={60}
        className="text-white text-sm animate-spin"
      />
      <h2 className="text-center font-light text-2xl text-white font-sans">
        Loading...
      </h2>
    </div>
  );
};

export default Loading;
