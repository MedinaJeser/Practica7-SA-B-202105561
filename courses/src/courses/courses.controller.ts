import {
    Body,
    Controller,
    Get,
    Post,
    Delete,
    Patch,
    Param,
    Query,
} from '@nestjs/common';
import { CoursesService } from './courses.service';
import { Course } from './schemas/course.schema';

@Controller('courses')
export class CoursesController {
    constructor(private readonly coursesService: CoursesService) { }

    @Post()
    async create(@Body() course: Course): Promise<Course> {
        return this.coursesService.create(course);
    }

    @Get()
    async findAll(): Promise<Course[]> {
        return this.coursesService.findAll();
    }

    @Get(':id')
    async findOne(@Param('id') id: string): Promise<Course | null> {
        return this.coursesService.findOne(id);
    }

    @Patch(':id')
    async update(
        @Param('id') id: string,
        @Body() course: Course,
    ): Promise<Course | null> {
        return this.coursesService.update(id, course);
    }

    @Delete(':id')
    async remove(@Param('id') id: string): Promise<Course | null> {
        return this.coursesService.remove(id);
    }
}
