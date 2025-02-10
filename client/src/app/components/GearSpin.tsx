import { faGear } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

const GearSpin = () => {
  return (
    <FontAwesomeIcon
      icon={faGear}
      width={60}
      height={60}
      className="text-white text-6xl animate-spin"
    />
  );
};

export default GearSpin;
