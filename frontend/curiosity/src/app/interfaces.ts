export interface Profile {
    profile_pic: string,
    user:
        {
            active: boolean,
            admin: boolean,
            date_created: string,
            email: string,
            first_name: string,
            last_name: string,
            staff: boolean,
            writer: boolean
        }
}

export interface writerProfile {
    writer_name: string,
    bio: string
}

export interface userRegistration {
    email: string,
    first_name: string,
    last_name: string,
    password: string
}


export interface post {
    id: number,
    slug: string,
    status: string,
    last_edited: string,
    summary: string,
    thumbnail: string,
    writer: string,
    title: string,
    content: string
}
