import { faGear } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

const GearSpin = () => {
  return (
    <FontAwesomeIcon
      icon={faGear}
      className="text-white text-5xl animate-spin"
    />
  );
};

export default GearSpin;
