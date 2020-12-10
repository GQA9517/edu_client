from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ("id", "name")


class TeacherModelSerializer(ModelSerializer):
    """讲师"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "signature", "image", "brief")


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list")


class CourseDetailModelSerializer(ModelSerializer):
    """课程详细信息的序列化器"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list", "course_category", "level_message",
                  "course_chapter_list", "brief_html", "file_path")
        # course_chapter_list  一级标题
        # lesson_list  二级标题
        extra_kwargs = {
            "level_message": {
                "read_only": True
            }
        }


class CourseLessonModelSerializer(ModelSerializer):
    """课程课时信息"""

    class Meta:
        model = CourseLesson
        fields = ['id', "name", "free_trail", "duration"]


class CourseChapterModelSerializer(ModelSerializer):
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'chapter', 'name', "coursesections"]
