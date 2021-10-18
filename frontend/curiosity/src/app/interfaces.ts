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


interface postBase {
    title: string,
    summary: string,
    thumbnail: string
}

export interface postEdit extends postBase {
    content: string
}

export interface postSummary extends postBase {
    id: number,
    slug: string,
    status: string,
    last_edited: string,
    writer: string,
    writer_id: string
}

export interface post extends postSummary {
    content: string,
    writer_profile_pic: string
}

export interface updateProfile {
    first_name: string,
    last_name: string,
    profile_pic: string
}

export interface InputEdit {
    label: string,
    id: string,
    value: string,
    onEdit: boolean,
}

export interface WriterApplicationResponse {
    email: string,
    user: string,
    approved: boolean | null,
    submitted_on: string,
    approved_by: string | null,
    bio: string,
    writings: string
}

export interface writerApplicationPending {
    application: boolean,
    data: WriterApplicationResponse
}

export class editInput {
    label = "";
    id = "";
    value = "";
    onEdit = false;

    constructor(label = "", id = "", value = "", onEdit = false) {
        this.label = label;
        this.id = id;
        this.value = value;
        this.onEdit = onEdit;
    }
}

