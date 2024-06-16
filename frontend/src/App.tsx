import ShortNavbar from "./components/ShortNavbar";
import ShortSidebar from "./components/ShortSidebar";
import ShortUrlList from "./components/ShortUrlList";

function App() {
  return (
    <main className="h-full">
      <ShortNavbar />
      <div className="flex h-full overflow-hidden bg-gray-50 pt-16 dark:bg-gray-900">
        <ShortSidebar />
        <div
          id="main-content"
          className="relative size-full overflow-y-auto bg-gray-50 dark:bg-gray-900 lg:ml-64"
        >
          <ShortUrlList />
        </div>
      </div>
    </main>
  );
}

export default App;
