import React, { FC } from "react";
import PanelButton from "./PanelButton";

interface IWarningProps {
  text?: string;
  link?: string;
  linkText?: string;
}

const Warning: FC<IWarningProps> = ({
  text = "You do not have permission to view this page.",
  link = "/",
  linkText = "Go back",
}) => {
  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <h2 className="text-center text-5xl text-white font-sans font-bold">
        {text}
      </h2>
      {link && linkText && (
        <PanelButton link={link} isLink text={linkText} />
      )}
    </div>
  );
};

export default Warning;
