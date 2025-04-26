import Link from "next/link";
import React, { FC } from "react";

interface IPanelButtons {
  text: string;
  onClick?: () => void;
  isLink?: boolean;
  link?: string;
}

const PanelButton: FC<IPanelButtons> = ({
  text,
  isLink = false,
  link = "/",
  onClick,
}) => {
  return isLink ? (
    <Link
      href={link}
      className="bg-[#786483] border-b-4 text-white border-neutral-800 hover:bg-white hover:text-black md:text-lg rounded-lg px-2 py-1 m-2 hover:scale-110 transition-all duration-200 font-semibold cursor-pointer"
    >
      {text}
    </Link>
  ) : (
    <button
      className="bg-[#786483] border-b-4 text-white border-neutral-800 hover:bg-white hover:text-black md:text-lg rounded-lg px-2 py-1 m-2 hover:scale-110 transition-all duration-200 font-semibold cursor-pointer"
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default PanelButton;
