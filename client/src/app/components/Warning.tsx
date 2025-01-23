import Link from "next/link";
import React, { FC } from "react";

interface IWarningProps {
  text?: string;
  link?: string;
  linkText?: string;
}

const Warning: FC<IWarningProps> = ({
  text = "This is a warning message.",
  link = null,
  linkText = null,
}) => {
  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <h2 className="text-center text-5xl text-white font-sans font-bold">
        {text}
      </h2>
      {link && linkText && (
        <Link
          href={link}
          className="bg-purple-700 hover:bg-purple-500 hover:scale-110 transition-all duration-300 text-white font-bold py-2 px-4 rounded mt-4 select-none"
        >
          {linkText}
        </Link>
      )}
    </div>
  );
};

export default Warning;
