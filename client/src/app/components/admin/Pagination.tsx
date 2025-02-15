import { faCircleLeft, faCircleRight } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React, { FC } from "react";

interface IPaginationProps {
  currentPage: number;
  totalPages: number;
  url: string;
}

const Pagination: FC<IPaginationProps> = ({ currentPage, totalPages, url }) => {
  const clamp = (value: number, min: number, max: number) => Math.min(Math.max(value, min), max);

  return (
    <div className="flex items-center justify-center">
      <Link href={url + (clamp(currentPage - 1, 1, totalPages))}>
        <FontAwesomeIcon icon={faCircleLeft} color="white" style={{width: "30px", height: "30px"}} className="mr-2" />
      </Link>
      {Array.from({ length: totalPages }, (_, index) => (
        <Link
          className={`mx-2 text-xl font-light hover:scale-125 hover:text-white transition-transform duration-300 ${
            index === currentPage - 1 ? "text-white underline" : "text-gray-400"
          }`}
          key={index}
          href={url + (index + 1)}
        >
          {index + 1}
        </Link>
      ))}
      <Link href={url + (clamp(currentPage + 1, 1, totalPages))}>
        <FontAwesomeIcon icon={faCircleRight} color="white" style={{width: "30px", height: "30px"}} className="ml-2" />
      </Link>
    </div>
  );
};

export default Pagination;
