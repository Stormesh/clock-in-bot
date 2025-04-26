import React, { FC } from "react";

interface IButtonProps {
  text: string;
  clickEvent: () => void;
}

const AdminButton: FC<IButtonProps> = ({
  text,
  clickEvent,
}) => {
  return (
    <button
      onClick={clickEvent}
      className={`bg-[#786483] hover:bg-white hover:text-black hover:scale-95 cursor-pointer font-bold transition-all rounded-lg p-1 m-1`}
    >
      {text}
    </button>
  );
};

export default AdminButton;
