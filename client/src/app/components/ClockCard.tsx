import React, { FC } from "react";
import Image from "next/image";
import styles from "@/styles/clock.module.css";

interface UserProps {
  name: string;
  avatar: string;
  clockTime: number;
  meetingTime: number;
  breakTime: number;
  isClockedIn: boolean;
  onBreak: boolean;
  onMeeting: boolean;
}

const ClockCard: FC<UserProps> = ({
  name,
  avatar,
  clockTime,
  meetingTime,
  breakTime,
  isClockedIn,
  onBreak,
  onMeeting,
}) => {
  const setZeros = (num: number) => {
    return num < 10 ? `0${num}` : num;
  };

  const timeFormat = (time: number) => {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = time % 60;
    return `${setZeros(hours)}:${setZeros(minutes)}:${setZeros(seconds)}`;
  };

  const timeElement = (time: number, effect: boolean, emoji: string) => {
    return (
      <td className="text-violet-200 font-mono">
        {timeFormat(time)}
        <span
          className={effect ? styles.onEffect : "hidden"}
          aria-hidden={!effect}
        >
          {emoji}
        </span>
      </td>
    );
  };

  return (
    <tr className="bg-cardBg even:bg-[#3b3553] border-2 border-tableBorder">
      <td>
        <div className="mx-3 my-1">
          <Image
            className="rounded-full place-self-center m-1 hover:scale-110 transition-transform"
            src={avatar}
            alt={name}
            width={100}
            height={100}
          />
          <p className="text-violet-300 font-sans font-light">{name}</p>
        </div>
      </td>
      {timeElement(clockTime, isClockedIn, "🕒")}
      {timeElement(meetingTime, onMeeting, "📅")}
      {timeElement(breakTime, onBreak, "☕")}
    </tr>
  );
};

export default ClockCard;
