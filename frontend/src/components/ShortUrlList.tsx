import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeadCell,
  TableRow,
} from "flowbite-react";
import React, { useEffect, useState } from "react";

interface Url {
  shortkey: string;
  url: string;
  date_created: string;
}

const ShortUrlList: React.FC = () => {
  const [urls, setUrls] = useState<Url[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUrls = async () => {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/urls`,
        );
        if (!response.ok) {
          throw new Error("Failed to fetch URLs");
        }
        const data: Url[] = await response.json();
        setUrls(data);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUrls();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="overflow-x-auto p-4">
      <Table>
        <TableHead>
          <TableHeadCell>Short URL</TableHeadCell>
          <TableHeadCell>URL</TableHeadCell>
          <TableHeadCell>Date Created</TableHeadCell>
        </TableHead>
        <TableBody className="divide-y">
          {urls.map((url) => (
            <TableRow
              className="bg-white dark:border-gray-700 dark:bg-gray-800"
              key={url.shortkey}
            >
              <TableCell>
                <a
                  href={`${process.env.REACT_APP_BACKEND_DOMAIN}/${url.shortkey}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  {process.env.REACT_APP_BACKEND_DOMAIN}/{url.shortkey}
                </a>
              </TableCell>
              <TableCell>{url.url}</TableCell>
              <TableCell>
                {new Date(url.date_created).toLocaleString()}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default ShortUrlList;
