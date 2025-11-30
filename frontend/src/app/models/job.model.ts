export interface Company {
  name: string;
  description: string;
  company_link: string;
  contact_email: string;
  phone_number: string;
}

export interface Job {
  job_title: string;
  job_location: string;
  job_id: string;
  job_link: string;
  salary: string;
  allows_c2c: boolean;
  company: Company;
}

export interface JobsResponse {
  jobs: Job[];
  total: number;
  filters: {
    query: string | null;
    c2c: string | null;
    has_email: string | null;
  };
}

export interface JobsFullResponse {
  search_query: string;
  search_location: string;
  scraped_at: string;
  total_jobs: number;
  details_extracted_at: string;
  emails_extracted_at: string;
  emails_found: number;
  c2c_jobs_found: number;
  jobs: Job[];
}
