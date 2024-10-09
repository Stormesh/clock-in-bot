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

  const showEffect = (effect: boolean, emoji: string) => {
    return effect ? <span className={styles.onEffect}>{emoji}</span> : null;
  }

  return (
    <tr>
      <td>
        <div>
          <Image
            className={styles.userAvatar}
            src={avatar}
            alt={name}
            width={100}
            height={100}
          />
        </div>
        <span className={styles.userName}>{name}</span>
      </td>
      <td>
        {timeFormat(clockTime)}
        {showEffect(isClockedIn, "⏲️")}
      </td>
      <td>
        {timeFormat(meetingTime)}
        {showEffect(onMeeting, "📅")}
      </td>
      <td>
        {timeFormat(breakTime)}
        {showEffect(onBreak, "🍔")}
      </td>
    </tr>
  );
};

export default ClockCard;
