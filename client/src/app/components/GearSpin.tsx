import { faGear } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

const GearSpin = () => {
  return (
    <FontAwesomeIcon
      icon={faGear}
      style={{ width: "60px", height: "60px" }}
      className="text-white animate-spin"
    />
  );
};

export default GearSpin;
