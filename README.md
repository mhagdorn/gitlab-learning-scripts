# GitLab Learning Scripts

A collection of scripts that use the [GitLab REST API](https://docs.gitlab.com/ee/api/rest/) to setup GitLab projects and repositories for a group of students. The functionality is inspired by [GitHub Classroom](https://classroom.github.com/) but more light-weight without a graphical user interface. Courses are defined via yaml configuration files. See the [course.yml](course.yml) for an example course description.


## Concepts

- **Roles**: 
  - teacher: *owner* of project
  - helper: *reporter*, they get to see the code and handle issues
  - students: are only added to individual projects/repositories
  
- **Functionality**:
  - the system is idempotent
  - a course is mapped to a private GitLab group
  - each project has a least a `personal` subgroup which contains repositories for the individual students. 
  - student group projects are mapped to repositories in a subgroup. Students are added to their respective repositories
  - have private instructor repositories that the personal/group repositories are cloned from

