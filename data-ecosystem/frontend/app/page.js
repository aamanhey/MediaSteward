import Image from "next/image";
import styles from "./page.module.css";
import GraphPage from "./pages/index";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Image
          className={styles.logo}
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <h1 className={styles.title}>
          Welcome to <a href="https://nextjs.org">My site!</a>
        </h1>
        <GraphPage />
      </main>
      <footer className={styles.footer}>
      </footer>
    </div>
  );
}

