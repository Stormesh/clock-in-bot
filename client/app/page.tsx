import ClockList from "./components/ClockList";
import styles from "./page.module.css"

export default function Home() {
  return (
    <div className={styles.main}>
      <ClockList />
    </div>
  );
}
