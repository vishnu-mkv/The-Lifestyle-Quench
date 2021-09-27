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
