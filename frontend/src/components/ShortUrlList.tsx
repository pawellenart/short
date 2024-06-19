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
  title: string;
  date_created: string;
}

interface UrlResponse {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  urls: Url[];
}

const ShortUrlList: React.FC = () => {
  const [urls, setUrls] = useState<Url[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);
  const [sortBy, setSortBy] = useState<string>("date_created");
  const [sortOrder, setSortOrder] = useState<string>("desc");
  const [totalPages, setTotalPages] = useState<number>(1);

  const apiKey = process.env.REACT_APP_API_KEY;

  useEffect(() => {
    const fetchUrls = async () => {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/urls?api_key=${apiKey}&page=${page}&page_size=${pageSize}&sort_by=${sortBy}&sort_order=${sortOrder}`,
        );
        if (!response.ok) {
          throw new Error("Failed to fetch URLs");
        }
        const data: UrlResponse = await response.json();
        setUrls(data.urls);
        setTotalPages(data.total_pages);
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
  }, [page, pageSize, sortBy, sortOrder]);

  const handlePageChange = (newPage: number) => {
    if (newPage > 0 && newPage <= totalPages) {
      setPage(newPage);
    }
  };

  const handlePageSizeChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setPageSize(Number(event.target.value));
  };

  const handleSortChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const [sort, order] = event.target.value.split(":");
    setSortBy(sort);
    setSortOrder(order);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="overflow-x-auto p-4">
      <Table hoverable>
        <TableHead>
          <TableHeadCell>Short URL</TableHeadCell>
          <TableHeadCell>URL</TableHeadCell>
          <TableHeadCell>Title</TableHeadCell>
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
              <TableCell>{url.title}</TableCell>
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
