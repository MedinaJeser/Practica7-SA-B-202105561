import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Course, CourseDocument } from './schemas/course.schema';

@Injectable()
export class CoursesService {
    constructor(
        @InjectModel(Course.name) private courseModel: Model<CourseDocument>,
    ) { }

    async create(course: Course): Promise<Course> {
        const newCourse = new this.courseModel(course);
        return newCourse.save();
    }

    async findAll(): Promise<Course[]> {
        return this.courseModel.find().exec();
    }

    async findOne(id: string): Promise<Course | null> {
        return this.courseModel.findById(id).exec();
    }

    async update(id: string, course: Course): Promise<Course | null> {
        return this.courseModel.findByIdAndUpdate(id, course, { new: true }).exec();
    }

    async remove(id: string): Promise<Course | null> {
        return this.courseModel.findByIdAndDelete(id).exec();
    }
}
