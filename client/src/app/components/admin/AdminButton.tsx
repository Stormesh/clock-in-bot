import React, { FC } from "react";

interface IButtonProps {
  bgColor: string;
  hoverColor: string;
  text: string;
  clickEvent: () => void;
}

const AdminButton: FC<IButtonProps> = ({
  bgColor,
  hoverColor,
  text,
  clickEvent,
}) => {
  return (
    <button
      onClick={() => clickEvent}
      className={`${bgColor} ${hoverColor} hover:scale-95 font-bold transition-all rounded-lg p-1 m-1`}
    >
      {text}
    </button>
  );
};

export default AdminButton;
